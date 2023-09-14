import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="12345678")

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS todos')
cur.execute(
        """CREATE TABLE todos (
           id SERIAL PRIMARY KEY,
           user_id VARCHAR(255) NOT NULL,
           title VARCHAR(255) NOT NULL,
           description TEXT,
           time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

conn.commit()

cur.close()
conn.close()
