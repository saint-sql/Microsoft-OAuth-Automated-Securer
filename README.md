<p align="center">
  <img src="https://avatars.githubusercontent.com/u/231521105?s=400&u=7a1e25fdf7a1b5e1b4872ada8b595a9d859c0f26&v=4" width="180" alt="Profile Picture"/>
</p>

<h1 align="center">Securer</h1>

<p align="center">
  <strong>Saint's Microsoft OAuth Securer</strong><br>
  Powered by Saint + Azure ®
</p>

<p align="center">
  <a href="https://github.com/saint-sql/dualhook-web/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/saint-sql/dualhook-web?style=social">
  </a>
  <a href="https://github.com/saint-sql/dualhook-web/forks">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/saint-sql/dualhook-web?style=social">
  </a>
</p>

<p align="center">
  Made by <strong>saint-sql</strong> 🇬🇧 | 20 | CyberSec Enthusiast
</p>

---

## Features
- Check MFA, devices, OAuth apps, and account info
  + Shows which MFA methods are enabled
  + Lists all registered devices
  + Lists all authorized OAuth apps

- Secure login via Microsoft Device Code flow
   + Uses Microsoft Azure OAuth and Tenant ID
   + No passwords are ever stored
    
- Token caching
  + Saves login token locally for convenience
  + Automatically refreshes when needed
   
- Export audit reports to JSON
  + Can save and share reports easily
  + Keeps a record of account audit history

- GUI EXE for Windows (built with PyInstaller)
  + Simple, easy-to-use interface
  + No Python installation required

- Smooth, threaded GUI so it doesn’t freeze
  + Very responsive even during long audits
  + Threads handle network calls in the background

- Device code copied to clipboard automatically
  + Makes logging in faster and easier

- Opens browser to Microsoft login page automatically
  + No need to manually go to login page

## Usage
Python version

Clone the repo:
```bash
git clone https://github.com/saint-sql/Microsoft-OAuth-Automated-Securer.git
```
# Install dependencies:
```bash
pip install -r requirements.txt
```
# Run the OAuth:
```bash
python saintsecure.py
```

# Windows EXE

Download the EXE from the Releases tab.
Double-click to run — no Python needed.

