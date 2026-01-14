import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from threading import Thread
import webbrowser
import os
import msal
import json
import requests
import pyperclip
from colorama import init, Fore

init(autoreset=True)


# Config
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
TENANT = "consumers"
SCOPES = ["User.Read"]
TOKEN_CACHE_FILE = "token_cache.json"
GRAPH = "https://graph.microsoft.com/v1.0"


# OAuth

def get_token():
    """Obtain Microsoft token, with caching."""
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        cache.deserialize(open(TOKEN_CACHE_FILE, "r").read())

    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT}",
        token_cache=cache
    )

    
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("Failed to create device flow")

   
    webbrowser.open(flow['verification_uri'])
    
    pyperclip.copy(flow['user_code'])

    # Return flow and app for GUI to handle
    return flow, app



def audit_account(token, export=False):
    headers = {"Authorization": f"Bearer {token}"}

    # User info
    user = requests.get(f"{GRAPH}/me", headers=headers).json()
    info = []
    info.append(Fore.CYAN + "\n🔍 ACCOUNT INFO")
    info.append(Fore.YELLOW + f"Name: {user.get('displayName')}")
    info.append(Fore.YELLOW + f"Email: {user.get('userPrincipalName')}")
    info.append(Fore.YELLOW + f"Account ID: {user.get('id')}")

    # MFA / auth methods
    try:
        auth_methods = requests.get(f"{GRAPH}/me/authentication/methods", headers=headers).json()
        if 'value' in auth_methods:
            mfa_enabled = any(method['methodType'] in ['microsoftAuthenticator', 'phone', 'email'] 
                              for method in auth_methods.get('value', []))
            info.append(Fore.GREEN + "MFA enabled: ✅ Yes" if mfa_enabled else Fore.RED + "MFA enabled: ❌ No")
        else:
            info.append(Fore.RED + "MFA enabled: ❌ Not available for this account")
    except:
        info.append(Fore.RED + "MFA enabled: ❌ Not available for this account")

    # Devices
    try:
        devices = requests.get(f"{GRAPH}/me/devices", headers=headers).json().get('value', [])
        if devices is not None and len(devices) > 0:
            info.append(Fore.CYAN + f"Number of registered devices: {len(devices)}")
            for d in devices:
                info.append(Fore.YELLOW + f" - {d.get('displayName')} ({d.get('operatingSystem')})")
        else:
            info.append(Fore.RED + "Number of registered devices: ❌ Not available for this account")
    except:
        info.append(Fore.RED + "Number of registered devices: ❌ Not available for this account")

    if export:
        with open("audit_report.json", "w") as f:
            json.dump(info, f, indent=2)

    return "\n".join(info)



class AutoSecureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoSecure Pro Safe Edition")
        self.root.geometry("800x600")
        self.token = None

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))

        
        self.tabs = ttk.Notebook(root)
        self.tab_audit = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_audit, text="Audit")
        self.tabs.pack(expand=1, fill="both")

        
        self.login_btn = ttk.Button(self.tab_audit, text="Login with Microsoft", command=self.login)
        self.login_btn.pack(pady=10)

        
        self.audit_output = scrolledtext.ScrolledText(self.tab_audit, width=95, height=25, state=tk.DISABLED)
        self.audit_output.pack(padx=10, pady=5)

        
        self.full_audit_btn = ttk.Button(self.tab_audit, text="Run Full Security Audit", command=self.run_full_audit, state=tk.DISABLED)
        self.full_audit_btn.pack(pady=5)

    
    
    def run_in_thread(self, func):
        Thread(target=func, daemon=True).start()

    # LOGIN
    def login(self):
        self.run_in_thread(self._login)

    def _login(self):
        try:
            result = get_token()
            if isinstance(result, tuple):
                flow, app = result

                # Show device code popup on main thread
                self.root.after(0, lambda: messagebox.showinfo(
                    "Device Code Login",
                    f"{flow['message']}\n\nThe code is copied to your clipboard!"
                ))

                # Acquire token (blocking until user enters code)
                token_result = app.acquire_token_by_device_flow(flow)
                if "access_token" not in token_result:
                    raise Exception("Authentication failed")
                self.token = token_result["access_token"]
            else:
                self.token = result

            # Enable buttons and show success on main thread
            self.root.after(0, self.enable_buttons)
            self.root.after(0, lambda: messagebox.showinfo("Login Success", "Microsoft login successful!"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Login Failed", str(e)))

    def enable_buttons(self):
        self.full_audit_btn.config(state=tk.NORMAL)

 
    
    def run_full_audit(self):
        self.run_in_thread(self._run_full_audit)

    def _run_full_audit(self):
        if not self.token:
            self.root.after(0, lambda: messagebox.showwarning("Not logged in", "Please login first."))
            return
        self.audit_output.config(state=tk.NORMAL)
        self.audit_output.delete("1.0", tk.END)
        output = audit_account(self.token)
        self.audit_output.insert(tk.END, output)
        self.audit_output.config(state=tk.DISABLED)

# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SaintSecureGUI(root)
    root.mainloop()
