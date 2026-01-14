import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)  # Auto-reset colors

GRAPH = "https://graph.microsoft.com/v1.0"

def audit_account(token, export=False):
    headers = {"Authorization": f"Bearer {token}"}

    report = {}

    # Basic account info
    user = requests.get(f"{GRAPH}/me", headers=headers).json()
    report['Name'] = user.get('displayName')
    report['Email'] = user.get('userPrincipalName')
    report['Account ID'] = user.get('id')

    print(Fore.CYAN + "\n🔍 ACCOUNT INFO")
    print(Fore.YELLOW + f"Name: {report['Name']}")
    print(Fore.YELLOW + f"Email: {report['Email']}")
    print(Fore.YELLOW + f"Account ID: {report['Account ID']}")

    # MFA & authentication methods
    auth_methods = requests.get(f"{GRAPH}/me/authentication/methods", headers=headers).json()
    report['Auth Methods Count'] = len(auth_methods.get('value', []))
    print(Fore.CYAN + f"Number of authentication methods: {report['Auth Methods Count']}")

    mfa_enabled = any(method['methodType'] in ['microsoftAuthenticator', 'phone', 'email'] 
                      for method in auth_methods.get('value', []))
    report['MFA Enabled'] = mfa_enabled
    print(Fore.GREEN + "MFA enabled: ✅ Yes" if mfa_enabled else Fore.RED + "MFA enabled: ❌ No")

    # Devices
    devices = requests.get(f"{GRAPH}/me/devices", headers=headers).json().get('value', [])
    report['Devices'] = [{"Name": d.get('displayName'), "OS": d.get('operatingSystem')} for d in devices]
    print(Fore.CYAN + f"Number of registered devices: {len(devices)}")
    for d in devices:
        print(Fore.YELLOW + f" - {d.get('displayName')} ({d.get('operatingSystem')})")

    # OAuth apps
    apps = requests.get(f"{GRAPH}/me/oauth2PermissionGrants", headers=headers).json().get('value', [])
    report['OAuth Apps'] = [app.get('clientId') for app in apps]
    print(Fore.CYAN + f"Number of OAuth apps granted permissions: {len(apps)}")
    for app in apps:
        print(Fore.YELLOW + f" - {app.get('clientId')}")

    # Export if requested
    if export:
        filename = f"audit_report.json"
        with open(filename, "w") as f:
            json.dump(report, f, indent=4)
        print(Fore.GREEN + f"\n✅ Audit report exported to {filename}")
