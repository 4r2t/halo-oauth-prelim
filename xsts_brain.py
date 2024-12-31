import asyncio
from xblheadlessoauthxsts import automate_xsts_oauth_login
from xsts_token import get_xbox_token, authenticate_xbox_live, get_xsts_token

# Define your client_id, client_secret, and user credentials
client_id = os.getenv("GTCID")
client_secret = os.getenv("GTCSEC")
username = os.getenv("MSXBLUSER")
password = os.getenv("MSXBLPASS")

# Function to save the XSTS token and user_hash (correctly from DisplayClaims)
def save_token_to_file(token, user_hash, filename="xsts_token.txt"):
    with open(filename, 'w') as file:
        file.write(f"{user_hash};{token}")
    print(f"XSTS token and user_hash saved to {filename}")

# Main function to run the OAuth and XSTS token chain
async def main():
    # Step 1: Automate the OAuth login to get the XSTS authorization code
    xsts_auth_code = automate_xsts_oauth_login(client_id, username, password)
    
    if not xsts_auth_code:
        print("Failed to get the XSTS authorization code.")
        return        

    # Step 2: Get Xbox Live token and user_hash
    rps_ticket, user_hash = await get_xbox_token(client_id, client_secret, xsts_auth_code)
    
    if not rps_ticket or not user_hash:
        print("Failed to get Xbox Live token or user hash.")
        return

    # Step 3: Authenticate with Xbox Live using RpsTicket and user_hash
    xbox_live_response = await authenticate_xbox_live(rps_ticket, user_hash)
    if not xbox_live_response:
        print("Failed to authenticate with Xbox Live.")
        return

    user_token = xbox_live_response['Token']

    # Step 4: Use the user token to get the XSTS token
    xsts_token_response = await get_xsts_token(user_token)
    if not xsts_token_response:
        print("Failed to get XSTS token.")
        return

    xsts_token = xsts_token_response['Token']
    print(f"Successfully obtained XSTS token: {xsts_token}")

    # Correctly extract the 'uhs' from the DisplayClaims of the XSTS response
    correct_user_hash = xsts_token_response['DisplayClaims']['xui'][0]['uhs']
    print(f"Correct User Hash: {correct_user_hash}")
    
    # Save both the XSTS token and correct user_hash (uhs) to a file
    save_token_to_file(xsts_token, correct_user_hash)

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
