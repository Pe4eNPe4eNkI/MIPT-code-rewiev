import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="il_patio_db",
            user="postgres",
            password="root",
            host="db")

        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.conn.cursor()

        print(f'server version {cur.fetchone()}')

        cur.execute('''CREATE TABLE Menu (
            type_p TEXT,
            name_p VARCHAR(255),
            description TEXT,
            price TEXT,
            image TEXT
            )''')
        print('[INFO] database is started')
db = DataBase