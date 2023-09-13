from flask import Response
from keycloak import KeycloakAuthenticationError
from config import keycloak_openid

def resolve_auth_url(obj, info):
    auth_url = keycloak_openid.auth_url(
            redirect_uri="http://localhost:5000/auth/openid-connect/callback",
            scope="openid")

    return auth_url

def resolve_userinfo(obj, info, access_token):
    try:
        userinfo = keycloak_openid.userinfo(access_token)
    except KeycloakAuthenticationError:
        raise Exception('you must be logged in')

    return userinfo
