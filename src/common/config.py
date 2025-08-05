import sys

from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

KEYCLOAK_CFG = {
    "server_url": os.getenv("SERVER_URL"),
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "realm_name": os.getenv("REALM_NAME")
}