import os
from keycloak import KeycloakOpenID
from dotenv import load_dotenv

load_dotenv()

KC_HOSTNAME_URL = os.environ['KC_HOSTNAME_URL']

REALM_NAME = os.environ['REALM_NAME']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET_KEY = os.environ['CLIENT_SECRET_KEY']

keycloak_openid = KeycloakOpenID(
        server_url=KC_HOSTNAME_URL,
        client_id=CLIENT_ID,
        realm_name=REALM_NAME,
        client_secret_key=CLIENT_SECRET_KEY)
