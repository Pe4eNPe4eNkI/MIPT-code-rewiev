import sqlite3
from sqlite3 import Cursor
from parser import parse


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("IlPatio.db")
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS Pizza')
        cur.execute('''
        CREATE TABLE Pizza (
            name VARCHAR(255) PRIMARY KEY,
            desc TEXT,
            price TEXT
        )''')

    def insert(self):
        cursor = self.conn.cursor()
        for pizza in parse():
            cursor.execute(f'''
            INSERT INTO Pizza (name, desc, price) VALUES 
            ('{pizza['name']}', '{pizza['description']}', '{pizza['price']}')
            ''')

    def select(self) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM Pizza''')
        return cursor

    def __del__(self):
        self.conn.commit()
        self.conn.close()
