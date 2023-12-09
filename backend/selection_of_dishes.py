import socket
import time

import psycopg2
from flask import Flask

app = Flask(__name__)

OPTIONS = {
    'dbname': "il_patio_db",
    'user': "postgres",
    'password': "root",
    'host': "database",
}


def select_all_in_category(category):
    with psycopg2.connect(**OPTIONS) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Menu WHERE type_p =%s', (category,))
            return cursor.fetchall()


def selection(category: str, prise: int):
    select_all = select_all_in_category(category)
    return select_all


def wain_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect(('database', 5432))
            s.close()
            break
        except socket.error:
            time.sleep(0.1)


if __name__ == '__main__':
    wain_conn()
    while True:
        try:
            selection('Пицца', 0)
        except psycopg2.OperationalError:
            time.sleep(1)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
