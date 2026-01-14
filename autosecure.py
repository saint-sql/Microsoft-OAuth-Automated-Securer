from auth import get_token
from audit import audit_account
from harden import sign_out_everywhere, revoke_unused_oauth
from colorama import init, Fore

init(autoreset=True)

def main():
    print(Fore.CYAN + "=== AutoSecure (Max Level Safe Edition) ===")
    token = get_token()  # Microsoft login once

    while True:
        print(Fore.BLUE + """
==== MAIN MENU ====
1. Run Account Audit
2. Sign out from all sessions
3. Revoke OAuth apps (user-approved)
4. Export Audit Report
5. Exit
""")
        choice = input(Fore.YELLOW + "Select an option: ").strip()

        if choice == "1":
            audit_account(token)
        elif choice == "2":
            sign_out_everywhere(token)
        elif choice == "3":
            revoke_unused_oauth(token)
        elif choice == "4":
            audit_account(token, export=True)
        elif choice == "5":
            print(Fore.CYAN + "Exiting AutoSecure.")
            break
        else:
            print(Fore.RED + "Invalid option, try again.")

if __name__ == "__main__":
    main()
