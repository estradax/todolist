from graphql.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, GraphQLObjectType
from graphql.type.scalars import GraphQLBoolean, GraphQLString
from graphql.type.schema import GraphQLSchema

import resolvers

UserInfoType = GraphQLObjectType(
    name="UserInfoType",
    fields={
        "sub": GraphQLField(
            GraphQLNonNull(GraphQLString)
        ),
        "email_verified": GraphQLField(
            GraphQLNonNull(GraphQLBoolean)
        ),
        "preferred_username": GraphQLField(
            GraphQLNonNull(GraphQLString)
        ),
        "given_name": GraphQLField(
            GraphQLNonNull(GraphQLString)
        ),
        "family_name": GraphQLField(
            GraphQLNonNull(GraphQLString)
        )
    }
)

QueryRootType = GraphQLObjectType(
    name="QueryRoot",
    fields={
        'auth_url': GraphQLField(
            GraphQLNonNull(GraphQLString),
            resolver=resolvers.resolve_auth_url,
        ),
        'userinfo': GraphQLField(
            UserInfoType,
            args={
                'access_token': GraphQLArgument(
                    GraphQLNonNull(GraphQLString)
                )
            },
            resolver=resolvers.resolve_userinfo
        )
    }
)

Schema = GraphQLSchema(QueryRootType)
