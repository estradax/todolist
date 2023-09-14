from graphql import GraphQLError
from keycloak import KeycloakAuthenticationError

from config import keycloak_openid

class AuthorizationMiddleware:
    def resolve(self, next, root, info, **args):
        if root is not None: return next(root, info, **args)

        # excluding auth_url as not protected endpoint
        if info.field_name in ['auth_url', 'delete_todo']: return next(root, info, **args)

        authorization = info.context.authorization
        if authorization is None:
            raise GraphQLError("You must be authorized")

        try:
            userinfo = keycloak_openid.userinfo(authorization.token)
        except KeycloakAuthenticationError:
            raise GraphQLError('You must be authorized')

        info.context.userinfo = userinfo

        return next(root, info, **args)


