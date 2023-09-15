import stripe
from graphql import GraphQLError

from config import keycloak_openid
from helpers import get_db, close_db, db_result_to_dict

stripe.api_key = 'sk_test_51LJaqkIfl5WCsiyEYxbjSAot43l9dNmG9RwJdt6vteaVLXi50iPamQgth1eB5lV1wPy0XaOxd43b5E92ZtWtjadw00YgKfdJdl'

def resolve_auth_url(obj, info): # pyright: ignore
    auth_url = keycloak_openid.auth_url(
            redirect_uri="http://localhost:5000/auth/openid-connect/callback",
            scope="openid")

    return auth_url

def resolve_publishable_key(obj, info): # pyright: ignore
    return 'pk_test_51LJaqkIfl5WCsiyEUdVuDg0zRLd3pUXgRcO2hCjdPOmoSmSsHyOxTvbr0uIJdlmGIXmobRDVydxTcKL3RBBqt1vy001f4SIzbT'

def resolve_create_checkout_session(obj, info): # pyright: ignore
    checkout_session = stripe.checkout.Session.create(
            success_url='http://localhost:5173' + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5000' + '/canceled.html',
            mode='payment',
            # automatic_tax={'enabled': True},
            line_items=[{
                'quantity': 1,
                'price': 'price_1NqWIhIfl5WCsiyEsZDFzTOl',
            }]
        )

    return checkout_session.url

def resolve_checkout_session(obj, info, sessionId): # pyright: ignore
    try:
        checkout_session = stripe.checkout.Session.retrieve(sessionId)
    except Exception as e:
        raise GraphQLError(str(e))

    if checkout_session.status != 'complete':
        return 'incomplete' 

    conn, cur = get_db() 

    user_id = info.context.userinfo.get('sub')

    cur.execute('SELECT * FROM pro_users WHERE user_id = %s', (user_id,))

    if cur.rowcount == 1:
        close_db(conn, cur)
        return 'complete'

    cur.execute('INSERT INTO pro_users(user_id) VALUES (%s)', (user_id,))
    conn.commit()

    close_db(conn, cur)

    return 'complete'

def resolve_userinfo(obj, info): # pyright: ignore
    return info.context.userinfo

def resolve_is_pro(obj, info): # pyright: ignore
    user_id = info.context.userinfo.get('sub')

    conn, cur = get_db()

    cur.execute('SELECT * FROM pro_users WHERE user_id = %s', (user_id,))

    is_pro = cur.rowcount == 1

    close_db(conn, cur)

    return is_pro

def resolve_todos(obj, info): # pyright: ignore
    conn, cur = get_db()

    user_id = info.context.userinfo.get('sub')

    cur.execute('SELECT * FROM todos WHERE user_id = %s ORDER BY time DESC', (user_id,)) 

    todos = db_result_to_dict(cur)

    close_db(conn, cur)

    return todos

def resolve_create_todo(obj, info, input): # pyright: ignore
    conn, cur = get_db()

    user_id = info.context.userinfo.get('sub')

    cur.execute('INSERT INTO todos(user_id, title, description) VALUES(%s, %s, %s) RETURNING *', 
                (user_id, input.get('title'), input.get('description')))

    todo = db_result_to_dict(cur)

    image = input.get('image')
    if info.context.is_pro and image:
        cur.execute('UPDATE todos SET image = %s WHERE id = %s', (image, todo[0].get('id')))

    conn.commit()

    close_db(conn, cur)

    return todo[0]

def resolve_update_todo(obj, info, id, input): # pyright: ignore
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

def resolve_delete_todo(obj, info, id): # pyright: ignore
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
