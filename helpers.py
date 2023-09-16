import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

def get_db():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password=POSTGRES_PASSWORD)
    cur = conn.cursor()

    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()

def db_result_to_dict(cur):
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


