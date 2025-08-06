import requests
from typing import Dict, Any, Optional
from common.config import KEYCLOAK_CFG


class KeycloakClient:
    def __init__(self):
        self.server_url = KEYCLOAK_CFG["server_url"]
        self.username = KEYCLOAK_CFG["username"]
        self.password = KEYCLOAK_CFG["password"]
        self.realm_name = KEYCLOAK_CFG["realm_name"]
        self.client_id = KEYCLOAK_CFG["client_id"]
        self.client_secret = KEYCLOAK_CFG["client_secret"]
        self.token = None
        self.refresh_token = None
        
    def _get_token(self) -> str:
        """Get access token using username and password"""
        # Try new URL structure first, then fall back to old one
        token_url = f"{self.server_url}/auth/realms/{self.realm_name}/protocol/openid-connect/token"
        
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "client_id": "admin-cli"  # Using admin-cli for admin operations
        }
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        
        return self.token
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authorization token"""
        if not self.token:
            self._get_token()
            
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Make authenticated request to Keycloak API"""
        url = f"{self.server_url}/auth/admin/realms/{self.realm_name}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params
            )
            
            # If token expired, refresh and retry
            if response.status_code == 401:
                self._get_token()
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self._get_headers(),
                    json=data,
                    params=params
                )
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return None
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Keycloak API request failed: {str(e)}")