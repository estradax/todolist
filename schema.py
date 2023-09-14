from graphql.type.definition import GraphQLArgument, GraphQLField, GraphQLInputObjectField, GraphQLInputObjectType, GraphQLList, GraphQLNonNull, GraphQLObjectType
from graphql.type.scalars import GraphQLBoolean, GraphQLInt, GraphQLString
from graphql.type.schema import GraphQLSchema

import resolvers

UserInfoType = GraphQLObjectType(
    name="UserInfo",
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

TodoType = GraphQLObjectType(
    name="Todo",
    fields={
        'id': GraphQLField(GraphQLInt),
        'user_id': GraphQLField(GraphQLString),
        'title': GraphQLField(GraphQLString),
        'description': GraphQLField(GraphQLString),
        'time': GraphQLField(GraphQLString),
    }
)

CreateTodoInputType = GraphQLInputObjectType(
    name='CreateTodoInput',
    fields={
        'title': GraphQLInputObjectField(
            GraphQLNonNull(GraphQLString)
        ),
        'description': GraphQLInputObjectField(GraphQLString)
    }
)

UpdateTodoInputType = GraphQLInputObjectType(
    name='UpdateTodoInput',
    fields={
        'title': GraphQLInputObjectField(GraphQLString),
        'description': GraphQLInputObjectField(GraphQLString)
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
            resolver=resolvers.resolve_userinfo
        ),
        'todos': GraphQLField(
            GraphQLList(TodoType),
            resolver=resolvers.resolve_todos
        )
    }
)


MutationRootType = GraphQLObjectType(
        name="MutationRoot",
        fields={
            'create_todo': GraphQLField(
                TodoType,
                args={
                    'input': GraphQLArgument(
                        GraphQLNonNull(CreateTodoInputType)
                    )
                },
                resolver=resolvers.resolve_create_todo
            ),
            'update_todo': GraphQLField(
                TodoType,
                args={
                    'id': GraphQLArgument(
                        GraphQLNonNull(GraphQLInt)
                    ),
                    'input': GraphQLArgument(
                        GraphQLNonNull(UpdateTodoInputType)
                    ),
                },
                resolver=resolvers.resolve_update_todo
            ),
            'delete_todo': GraphQLField(
                GraphQLNonNull(GraphQLString),
                args={
                    'id': GraphQLArgument(
                        GraphQLNonNull(GraphQLInt)
                    ),
                },
                resolver=resolvers.resolve_delete_todo
            )
        }
)

Schema = GraphQLSchema(QueryRootType, MutationRootType)
