import aiohttp

# Function to get Xbox Live token (XBL3.0) and user_hash
async def get_xbox_token(client_id, client_secret, xsts_auth_code):
    url = "https://login.live.com/oauth20_token.srf"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": xsts_auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://localhost"
    }

    print("Sending token request with the following data:")
    print(data)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            print(f"Response Status: {response.status}")
            response_text = await response.text()
            print(f"Response Body: {response_text}")
            
            if response.status == 200:
                tokens = await response.json()
                access_token = tokens['access_token']
                user_hash = tokens['user_id']
                print(f"Access Token (RpsTicket): {access_token}")
                print(f"User Hash: {user_hash}")
                return access_token, user_hash
            else:
                print(f"Failed to exchange authorization code: {response.status}")
                return None, None

# Function to authenticate Xbox Live using RPS ticket and user_hash
async def authenticate_xbox_live(rps_ticket, user_hash):
    url = "https://user.auth.xboxlive.com/user/authenticate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={rps_ticket}",  # Prefix the RpsTicket with "d="
            "UserHash": user_hash  # Pass the UserHash dynamically
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_text = await response.text()
            if response.status == 200:
                print(f"Successfully authenticated to Xbox Live. Response: {response_text}")
                return await response.json()
            else:
                print(f"Failed to authenticate Xbox Live: {response.status}, {response_text}")
                return None

# Function to get XSTS token
async def get_xsts_token(user_token):
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    headers = {
        "x-xbl-contract-version": "1",
        "Content-Type": "application/json"
    }
    data = {
        "RelyingParty": "http://xboxlive.com",
        "TokenType": "JWT",
        "Properties": {
            "UserTokens": [user_token],  # Pass the user token dynamically
            "SandboxId": "RETAIL"
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_text = await response.text()
            if response.status == 200:
                print(f"Successfully obtained XSTS token. Response: {response_text}")
                return await response.json()
            else:
                print(f"Failed to get XSTS token: {response.status}, {response_text}")
                return None