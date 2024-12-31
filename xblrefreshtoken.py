import asyncio
import aiohttp

# Function to exchange the authorization code for access and refresh tokens
async def get_access_token(client_id, client_secret, auth_code):
    url = "https://login.live.com/oauth20_token.srf"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
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
                print(f"Access Token: {tokens['access_token']}")
                return tokens
            else:
                print(f"Failed to exchange authorization code: {response.status}")
                return None

# Function to refresh the access token using a refresh token
async def refresh_access_token(client_id, client_secret, refresh_token):
    url = "https://login.live.com/oauth20_token.srf"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://localhost"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                new_tokens = await response.json()
                print(f"New Access Token: {new_tokens['access_token']}")
                return new_tokens
            else:
                print(f"Failed to refresh token: {response.status}")
                return None

# Example asynchronous task to refresh the token periodically
async def token_refresh_task(client_id, client_secret, refresh_token):
    while True:
        new_tokens = await refresh_access_token(client_id, client_secret, refresh_token)
        if new_tokens:
            refresh_token = new_tokens['refresh_token']  # Update refresh token
            access_token = new_tokens['access_token']  # Get new access token

        # Wait for the token's validity duration, refresh tokens typically last 3600 seconds
        await asyncio.sleep(3600)  # Refresh every hour
