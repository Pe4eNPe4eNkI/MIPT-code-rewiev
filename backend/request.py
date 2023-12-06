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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
