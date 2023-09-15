import psycopg2

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


