import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from parser import parser


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="il_patio_db",
            user="postgres",
            password="root",
            host="db")

        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.conn.cursor()

        cur.execute('select version();')

        print(f'server version {cur.fetchone()}')

        cur.execute('DROP TABLE IF EXISTS Menu')
        cur.execute('''CREATE TABLE Menu (
            type TEXT,
            name VARCHAR(255),
            description TEXT,
            price TEXT,
            image TEXT
            )''')

    def insert(self):
        cursor = self.conn.cursor()
        menu = [parser.pizza_parse(), parser.pasta_parse(), parser.hot_dish_parse(), parser.salad_parse()]
        for val in menu:
            for elem in val:
                text = 'INSERT INTO Menu (type, name, description, price, image) VALUES (%s, %s, %s, %s, %s);'
                exec_tuple = (elem['type'], elem['name'], elem['description'], elem['price'], elem['image'])
                cursor.execute(text, exec_tuple)

    def select_all(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Menu')
        return cursor

    def select_category(self, category):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Menu WHERE type =%s', (category,))
        return cursor

    def select_elem(self, elem):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Menu WHERE name =%s', (elem,))
        return cursor

    def select_name(self, category):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM Menu WHERE type =%s', (category,))
        return cursor

    def select_all_category(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT type FROM Menu')
        return cursor
