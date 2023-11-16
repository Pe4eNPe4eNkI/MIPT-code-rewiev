import sqlite3
from sqlite3 import Cursor
from parser import pizza_parse, pasta_parse, hot_dish_parse, salad_parse


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("IlPatio.db", check_same_thread=False)
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS Menu')
        cur.execute('''CREATE TABLE Menu (
            type TEXT,
            name VARCHAR(255) PRIMARY KEY,
            desc TEXT,
            price TEXT
        )''')

    def insert(self):
        cursor = self.conn.cursor()
        menu = [pizza_parse(), pasta_parse(), hot_dish_parse(), salad_parse()]
        for val in menu:
            for elem in val:
                cursor.execute(f'''INSERT INTO Menu (type, name, desc, price) VALUES 
                ('{elem['type']}', '{elem['name']}', '{elem['description']}', '{elem['price']}')
                ''')

    def select_all(self) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM Menu''')
        return cursor

    def select_category(self, category) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute(f'''SELECT * FROM Menu WHERE type = "{category}"''')
        return cursor

    def select_elem(self, elem) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute(f'''SELECT * FROM Menu WHERE name = "{elem}"''')
        return cursor

    def select_name(self, category) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute(f'''SELECT name FROM Menu WHERE type = "{category}"''')
        return cursor

    def select_all_category(self) -> Cursor:
        cursor = self.conn.cursor()
        cursor.execute(f'''SELECT type FROM Menu''')
        return cursor

    def __del__(self):
        self.conn.commit()
        self.conn.close()
