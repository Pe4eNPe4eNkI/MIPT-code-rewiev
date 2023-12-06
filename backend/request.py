import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="il_patio_db",
    user="postgres",
    password="root",
    host="database")

cur = conn.cursor()


@app.route('/select_all')
def select_all():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Menu')
    conn.commit()
    return jsonify(list(map(list, cursor.fetchall())))


@app.route('/select_elem/<elem>')
def select_elem(elem):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Menu WHERE name_p =%s', (elem,))
    conn.commit()
    return jsonify(list(map(list, cursor.fetchall())))


@app.route('/select_name/<category>')
def select_name(category):
    cursor = conn.cursor()
    cursor.execute('SELECT name_p FROM Menu WHERE type_p =%s', (category,))
    conn.commit()
    return jsonify(list(map(list, cursor.fetchall())))
