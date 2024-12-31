import asyncio
from xblheadlessoauth import automate_oauth_login
from xblheadlessoauthxsts import automate_xsts_oauth_login
from xblrefreshtoken import get_access_token
from xsts_token import get_xbox_token, get_xsts_token
import os

# Define your client_id, client_secret, and user credentials
client_id = os.getenv("GTCID")
client_secret = os.getenv("GTCSEC")
username = os.getenv("MSXBLUSER")
password = os.getenv("MSXBLPASS")

# Main function to run the OAuth and XSTS token chain
async def main():
    # Step 1: Automate the OAuth login process for access and refresh tokens
    auth_code = automate_oauth_login(client_id, username, password)
    
    if not auth_code:
        print("Failed to get the authorization code.")
        return
    
    # Step 2: Get the access and refresh token
    token_data = await get_access_token(client_id, client_secret, auth_code)
    
    if not token_data:
        print("Failed to exchange authorization code for tokens.")
        return

    oauth_token = token_data['access_token']

    xsts_auth_code = automate_xsts_oauth_login(client_id, username, password)
    
    if not xsts_auth_code:
        print("Failed to get the xsts authorization code.")
        return        

    xsts_token_data = await get_xsts_access_token(client_id, client_secret, xsts_auth_code)

    if not xsts_token_data:
        print("Failed to exchange xsts authorization code for xsts tokens.")
        return

    xbox_oauth_token = xsts_token_data['access_token']

    # Step 3: Automate OAuth login again to get Xbox OAuth token
    xbox_token = await get_xbox_token(client_id, username, password)
    if not xbox_token:
        print("Failed to get Xbox Live token.")
        return

    # Step 4: Use the Xbox token to get the XSTS token
    xsts_token = await get_xsts_token(xbox_token)
    if not xsts_token:
        print("Failed to get XSTS token.")
        return

    print(f"Successfully obtained XSTS token: {xsts_token}")

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())