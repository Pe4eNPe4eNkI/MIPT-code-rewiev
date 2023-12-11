import random
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

OPTIONS = {
    'dbname': "il_patio_db",
    'user': "postgres",
    'password': "root",
    'host': "database"
}


@app.route('/select_elem/<elem>')
def select_elem(elem):
    with psycopg2.connect(**OPTIONS) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Menu WHERE name_p =%s', (elem,))
            return jsonify(list(map(list, cursor.fetchall())))


@app.route('/select_name/<category>')
def select_name(category):
    with psycopg2.connect(**OPTIONS) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT name_p FROM Menu WHERE type_p =%s', (category,))
            return jsonify(list(map(list, cursor.fetchall())))


@app.route('/select_all_in_category/<category>')
def select_all_in_category(category):
    with psycopg2.connect(**OPTIONS) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Menu WHERE type_p =%s', (category,))
            return jsonify(list(map(list, cursor.fetchall())))


def select_all_in_category(category):
    with psycopg2.connect(**OPTIONS) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Menu WHERE type_p =%s', (category,))
            return cursor.fetchall()


@app.route('/selection/<category>/<int:price>')
def selection(category: str, price: int):
    select_all = select_all_in_category(category)
    cur_price = 0
    cart = []
    indx = 0

    while cur_price <= price:
        item = random.choice(select_all)
        if item not in cart:
            if cur_price + item[3] <= price:
                cart.append(item)
                cur_price += item[3]
            else:
                indx += 1
        if indx == 30 and len(cart) == 0:
            return jsonify(list(map(list, [(1,)])))
        if indx + len(cart) == len(select_all):
            return jsonify(list(map(list, cart)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
