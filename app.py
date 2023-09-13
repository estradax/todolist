from flask import Flask, json, redirect, request
from flask_cors import CORS
from flask_graphql import GraphQLView

from schema import Schema
from config import keycloak_openid

app = Flask(__name__)
CORS(app)

app.add_url_rule(
            '/graphql', view_func=GraphQLView.as_view('graphql', schema=Schema)
        )

app.add_url_rule(
            '/graphiql', view_func=GraphQLView.as_view('graphiql', schema=Schema, graphiql=True)
        )

@app.route('/auth/openid-connect/callback')
def openid_connect_callback():
    code = request.args.get('code')
    if not code:
        return 'error code is none'

    token = keycloak_openid.token(
            grant_type='authorization_code',
            code=code,
            redirect_uri='http://localhost:5000/auth/openid-connect/callback')

    return redirect(f'http://localhost:5173/auth/cb?token={json.dumps(token)}')
