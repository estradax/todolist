from graphql import GraphQLError
import psycopg2

from config import keycloak_openid

def get_db():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password='12345678')
    cur = conn.cursor()

    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()

def db_result_to_dict(cur):
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows

def resolve_auth_url(obj, info):
    auth_url = keycloak_openid.auth_url(
            redirect_uri="http://localhost:5000/auth/openid-connect/callback",
            scope="openid")

    return auth_url

def resolve_userinfo(obj, info):
    return info.context.userinfo

def resolve_todos(obj, info):
    conn, cur = get_db()

    user_id = info.context.userinfo.get('sub')

    cur.execute('SELECT * FROM todos WHERE user_id = %s ORDER BY time DESC', (user_id,)) 

    todos = db_result_to_dict(cur)

    close_db(conn, cur)

    return todos

def resolve_create_todo(obj, info, input):
    conn, cur = get_db()

    user_id = info.context.userinfo.get('sub')

    cur.execute('INSERT INTO todos(user_id, title, description) VALUES(%s, %s, %s) RETURNING *', 
                (user_id, input.get('title'), input.get('description')))

    conn.commit()

    todo = db_result_to_dict(cur)

    close_db(conn, cur)

    return todo[0]

def resolve_update_todo(obj, info, id, input):
    conn, cur = get_db()

    user_id = info.context.userinfo.get('sub')

    # check if user is the owner its todo
    cur.execute('SELECT * FROM todos WHERE id = %s AND user_id = %s', (id, user_id))

    if cur.rowcount != 1:
        close_db(conn, cur)
        raise GraphQLError('You\'re not the owner of this post')

    title = input.get('title')
    if title is not None:
        cur.execute('UPDATE todos SET title = %s where id = %s RETURNING *', (title, id))

    description = input.get('description')
    if description is not None:
        cur.execute('UPDATE todos SET description = %s where id = %s RETURNING *', (description, id))

    conn.commit()

    todo = db_result_to_dict(cur)

    if cur.rowcount != 1:
        close_db(conn, cur)
        raise GraphQLError('Update not successfull')

    close_db(conn, cur)

    return todo[0]

def resolve_delete_todo(obj, info, id):
    conn, cur = get_db()

    user_id = info.context.userinfo.get('sub')

    # check if user is the owner its todo
    cur.execute('SELECT * FROM todos WHERE id = %s AND user_id = %s', (id, user_id))

    if cur.rowcount != 1:
        close_db(conn, cur)
        raise GraphQLError('You\'re not the owner of this post')

    cur.execute('DELETE FROM todos WHERE id = %s RETURNING *', (id,))

    conn.commit()

    if cur.rowcount != 1:
        close_db(conn, cur)
        raise GraphQLError('Delete not successfull')

    close_db(conn, cur)

    return 'success'
