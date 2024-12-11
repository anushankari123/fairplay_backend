import httpx
import jwt
import os


class TokenManager:
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    async def authenticate_with_google(self, code: str, redirect_uri: str) -> dict:
        """
        Exchange authorization code for access token.

        Args:
        - code (str): Authorization code from Google.
        - redirect_uri (str): Redirect URI registered with Google.

        Returns:
        - dict: Token response containing the access token.
        """
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        async with httpx.AsyncClient() as client:
            response = await client.post(self.GOOGLE_TOKEN_URL, data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            })
            response.raise_for_status()
            return response.json()

    async def decode_jwt_token(self, access_token: str) -> dict:
        """
        Retrieve user information from the access token.

        Args:
        - access_token (str): Google OAuth access token.

        Returns:
        - dict: User information decoded from the JWT.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.GOOGLE_USERINFO_URL, headers={
                "Authorization": f"Bearer {access_token}"
            })
            response.raise_for_status()
            return response.json()
