import httpx
from typing import Dict, Any, Optional
from ..common.config import KEYCLOAK_CFG
from ..common.const import DEFAULT_REALM, DEFAULT_REQUEST_TIMEOUT


class KeycloakClient:
    def __init__(self):
        self.server_url = KEYCLOAK_CFG["server_url"]
        self.username = KEYCLOAK_CFG["username"]
        self.password = KEYCLOAK_CFG["password"]
        self.realm_name = (
            KEYCLOAK_CFG["realm_name"] if KEYCLOAK_CFG["realm_name"] else DEFAULT_REALM
        )
        self.client_id = KEYCLOAK_CFG["client_id"]
        self.client_secret = KEYCLOAK_CFG["client_secret"]
        self.token = None
        self.refresh_token = None
        self._client = None

    async def _ensure_client(self):
        """Ensure httpx async client exists"""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=DEFAULT_REQUEST_TIMEOUT)
        return self._client

    async def _get_token(self) -> str:
        """Get access token using username and password"""
        # Try new URL structure first, then fall back to old one
        token_url = f"{self.server_url}/auth/realms/{self.realm_name}/protocol/openid-connect/token"

        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "client_id": "admin-cli",  # Using admin-cli for admin operations
        }

        client = await self._ensure_client()
        response = await client.post(token_url, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")

        return self.token

    async def _get_headers(self) -> Dict[str, str]:
        """Get headers with authorization token"""
        if not self.token:
            await self._get_token()

        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        skip_realm: bool = False,
        realm: Optional[str] = None,
    ) -> Any:
        """Make authenticated request to Keycloak API"""
        if skip_realm:
            url = f"{self.server_url}/auth/admin{endpoint}"
        else:
            # Use provided realm or fall back to configured realm
            target_realm = realm if realm is not None else self.realm_name
            url = f"{self.server_url}/auth/admin/realms/{target_realm}{endpoint}"

        try:
            client = await self._ensure_client()
            headers = await self._get_headers()

            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
            )

            # If token expired, refresh and retry
            if response.status_code == 401:
                await self._get_token()
                headers = await self._get_headers()
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params,
                )

            response.raise_for_status()

            if response.content:
                return response.json()
            return None

        except httpx.RequestError as e:
            raise Exception(f"Keycloak API request failed: {str(e)}")

    async def close(self):
        """Close the httpx client"""
        if self._client:
            await self._client.aclose()
            self._client = None
