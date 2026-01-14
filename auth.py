import msal

# Replace this with your Azure App Client ID
CLIENT_ID = "7a0d014c-7c24-46c6-8cde-a725bdd9d1f1"

AUTHORITY = "https://login.microsoftonline.com/consumers"

# Only include non-reserved scopes
SCOPES = [
    "User.Read"
]

def get_token():
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY
    )

    # Start Device Code Flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("Failed to create device flow")

    print(flow["message"])  # Shows URL + code for login

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise Exception("Authentication failed")

    return result["access_token"]
