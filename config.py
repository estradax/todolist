from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
        server_url='http://localhost:8080/auth',
        client_id='todolist',
        realm_name='love',
        client_secret_key='GjWURPmRmh1eOUxnMvLF68D1MKOgaYQx')
