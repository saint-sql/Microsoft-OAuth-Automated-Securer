import requests

def sign_out_everywhere(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/me/revokeSignInSessions"
    response = requests.post(url, headers=headers)
    if response.status_code == 204:
        print("✅ Signed out from all sessions")
    else:
        print("❌ Failed to sign out")

def revoke_unused_oauth(token):
    headers = {"Authorization": f"Bearer {token}"}
    apps = requests.get(f"https://graph.microsoft.com/v1.0/me/oauth2PermissionGrants", headers=headers).json().get('value', [])

    if not apps:
        print("No OAuth apps found.")
        return

    print(f"{len(apps)} OAuth apps found:")
    for i, app in enumerate(apps, 1):
        print(f"{i}. {app.get('clientId')}")

    confirm = input("Do you want to revoke ALL apps? Type YES to confirm: ")
    if confirm.strip().upper() == "YES":
        for app in apps:
            app_id = app['id']
            response = requests.delete(f"https://graph.microsoft.com/v1.0/oauth2PermissionGrants/{app_id}", headers=headers)
            if response.status_code == 204:
                print(f"✅ Revoked app {app.get('clientId')}")
            else:
                print(f"❌ Failed to revoke {app.get('clientId')}")
    else:
        print("Aborted app revocation.")
