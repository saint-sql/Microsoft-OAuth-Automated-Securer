# SaintSecure (Public Edition)

SaintSecure is a safe tool to check and secure your Microsoft account.
It uses Microsoft’s Device Code login, so no passwords are ever stored.

Basically, you run the script and it acts as an OAuth to microsoft using azure device flow code with your EntraID to ensure login

# Features

+ Check MFA, devices, OAuth apps, and account info

+ Secure login via Microsoft Device Code flow

+ Token caching (so you don’t have to log in every time)

+ Export audit reports to JSON

+ GUI EXE for Windows (built with PyInstaller)

+ Smooth, threaded GUI so it doesn’t freeze

+ Device code copied to clipboard automatically

+ Opens browser to Microsoft login page automatically

# How to use

Python version

Clone the repo:
git clone https://github.com/YOUR_USERNAME/AutoSecure.git


# Install dependencies:

pip install -r requirements.txt


# Run the GUI:

python saintsecure_gui.py

# Windows EXE

Download the EXE from the Releases tab.

Double-click to run — no Python needed.

# Disclaimer

This tool is safe and portfolio-ready.

No passwords are ever stored — all login uses Microsoft’s Device Code flow.

Use it appropriately, im not liable for any misuse
