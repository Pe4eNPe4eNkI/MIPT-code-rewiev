import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


print('[DATABASE] i am runnind')

conn = psycopg2.connect(
            database="il_patio_db",
            user="postgres",
            password="root",
            host="database")

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute('''CREATE TABLE Menu(
            type_p TEXT,
            name_p VARCHAR(255),
            description_p TEXT,
            price TEXT,
            image_p TEXT
            )''')
print('[INFO] database is started')
