from graphql import GraphQLError
from keycloak import KeycloakAuthenticationError

from config import keycloak_openid
from helpers import get_db, close_db

class AuthorizationMiddleware:
    def resolve(self, next, root, info, **args):
        if root is not None: return next(root, info, **args)

        # excluding auth_url as not protected endpoint
        if info.field_name in ['auth_url', 'publishable_key']: return next(root, info, **args)

        authorization = info.context.authorization
        if authorization is None:
            raise GraphQLError("You must be authorized")

        try:
            userinfo = keycloak_openid.userinfo(authorization.token)
        except KeycloakAuthenticationError:
            raise GraphQLError('You must be authorized')

        info.context.userinfo = userinfo

        conn, cur = get_db()

        user_id = userinfo.get('sub')
        
        cur.execute('SELECT * FROM pro_users WHERE user_id = %s', (user_id,))
        is_pro = cur.rowcount == 1

        close_db(conn, cur)

        info.context.is_pro = is_pro

        return next(root, info, **args)


