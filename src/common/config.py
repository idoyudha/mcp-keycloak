from dotenv import load_dotenv
import os

load_dotenv()

KEYCLOAK_CFG = {
    "server_url": os.getenv("SERVER_URL"),
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "realm_name": os.getenv("REALM_NAME"),
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET"),
}
