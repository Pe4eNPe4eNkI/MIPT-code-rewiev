import socket
import time
import urllib.request

import psycopg2
from bs4 import BeautifulSoup

OPTIONS = {
    'dbname': "il_patio_db",
    'user': "postgres",
    'password': "root",
    'host': "database"
}


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def parse(all_quotes, found_quotes, bs_obj):
    category = bs_obj.find('h1', {'class': 'category-name ptx-10'}).text
    for found_quote in found_quotes:
        quote_name = found_quote.find('div', {'class': 'product_carousel__title'}).text
        quote_desc = found_quote.find('div', {'class': 'product_carousel__description'}).text
        quote_price = found_quote.find('div', {'class': 'product_carousel__price'}).text
        find_img = found_quote.find('div', {'class': 'product_carousel__img'})
        quote_img = 'https://ilpatio.ru/' + find_img.find('img').get('src')

        all_quotes.append({
            'type_p': category,
            'name_p': ' '.join(quote_name.split()),
            'description_p': ' '.join(quote_desc.split()),
            'price': ' '.join(quote_price.split()),
            'image_p': quote_img  # ' '.join(format(ord(x), 'b') for x in quote_img)
        })


def pizza_parse():
    all_quotes = []

    for i in range(1, 3):
        request = urllib.request.urlopen(f'https://ilpatio.ru/category/pitstsa/?page={i}')
        html = request.read()
        bs_obj = BeautifulSoup(html, 'html.parser')
        found_quotes = bs_obj.find_all('div', {'class': 'product_list__item phx-15'})

        parse(all_quotes, found_quotes, bs_obj)

    return all_quotes


def pasta_parse():
    all_quotes = []
    for i in range(1, 3):
        request = urllib.request.urlopen(f'https://ilpatio.ru/category/pasta/?page={i}')
        html = request.read()
        bs_obj = BeautifulSoup(html, 'html.parser')
        found_quotes = bs_obj.find_all('div', {'class': 'product_list__item phx-15'})

        parse(all_quotes, found_quotes, bs_obj)

    return all_quotes


def hot_dish_parse():
    all_quotes = []
    request = urllib.request.urlopen(f'https://ilpatio.ru/category/goryachie-blyuda/')
    html = request.read()
    bs_obj = BeautifulSoup(html, 'html.parser')
    found_quotes = bs_obj.find_all('div', {'class': 'product_list__item phx-15'})

    parse(all_quotes, found_quotes, bs_obj)

    return all_quotes


def salad_parse():
    all_quotes = []
    request = urllib.request.urlopen(f'https://ilpatio.ru/category/salaty-i-zakuski/')
    html = request.read()
    bs_obj = BeautifulSoup(html, 'html.parser')
    found_quotes = bs_obj.find_all('div', {'class': 'product_list__item phx-15'})

    parse(all_quotes, found_quotes, bs_obj)

    return all_quotes


def insert():
    with psycopg2.connect(**OPTIONS) as conn:
        with conn.cursor() as cursor:
            menu = [pizza_parse(), pasta_parse(), hot_dish_parse(), salad_parse()]
            for val in menu:
                for elem in val:
                    text = '''INSERT INTO Menu (type_p, name_p, description_p, price, image_p) 
                    VALUES (%s, %s, %s, %s, %s) on conflict  (name_p) do nothing;'''
                    exec_tuple = (elem['type_p'], elem['name_p'], elem['description_p'], elem['price'], elem['image_p'])
                    cursor.execute(text, exec_tuple)
                    conn.commit()


def wain_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect(('db', 5432))
            s.close()
            break
        except socket.error:
            time.sleep(0.1)


if __name__ == '__main__':
    wain_conn()
    while True:
        try:
            insert()
            time.sleep(24 * 60 * 60)
        except psycopg2.OperationalError:
            time.sleep(1)
