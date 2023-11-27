import urllib.request
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def parse(all_quotes, found_quotes, bsObj):
    category = bsObj.find('h1', {'class': 'category-name ptx-10'}).text
    for found_quote in found_quotes:
        quote_name = found_quote.find('div', {'class': 'product_carousel__title'}).text
        quote_desc = found_quote.find('div', {'class': 'product_carousel__description'}).text
        quote_price = found_quote.find('div', {'class': 'product_carousel__price'}).text
        find_img = found_quote.find('div', {'class': 'product_carousel__img'})
        quote_img = 'https://ilpatio.ru/' + find_img.find('img').get('src')

        all_quotes.append({
            'type_p': category,
            'name_p': ' '.join(quote_name.split()),
            'description': ' '.join(quote_desc.split()),
            'price': ' '.join(quote_price.split()),
            'image': quote_img  # ' '.join(format(ord(x), 'b') for x in quote_img)
        })


def pizza_parse():
    all_quotes = []

    for i in range(1, 3):
        request = urllib.request.urlopen(f'https://ilpatio.ru/category/pitstsa/?page={i}')
        html = request.read()
        bsObj = BeautifulSoup(html, 'html.parser')
        found_quotes = bsObj.find_all('div', {'class': 'product_list__item phx-15'})

        parse(all_quotes, found_quotes, bsObj)

    return all_quotes


def pasta_parse():
    all_quotes = []
    for i in range(1, 3):
        request = urllib.request.urlopen(f'https://ilpatio.ru/category/pasta/?page={i}')
        html = request.read()
        bsObj = BeautifulSoup(html, 'html.parser')
        found_quotes = bsObj.find_all('div', {'class': 'product_list__item phx-15'})

        parse(all_quotes, found_quotes, bsObj)

    return all_quotes


def hot_dish_parse():
    all_quotes = []
    request = urllib.request.urlopen(f'https://ilpatio.ru/category/goryachie-blyuda/')
    html = request.read()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_quotes = bsObj.find_all('div', {'class': 'product_list__item phx-15'})

    parse(all_quotes, found_quotes, bsObj)

    return all_quotes


def salad_parse():
    all_quotes = []
    request = urllib.request.urlopen(f'https://ilpatio.ru/category/salaty-i-zakuski/')
    html = request.read()
    bsObj = BeautifulSoup(html, 'html.parser')
    found_quotes = bsObj.find_all('div', {'class': 'product_list__item phx-15'})

    parse(all_quotes, found_quotes, bsObj)

    return all_quotes


conn = psycopg2.connect(
            database="il_patio_db",
            user="postgres",
            password="root",
            host="db")

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()


def insert():
        cursor = conn.cursor()
        menu = [pizza_parse(), pasta_parse(), hot_dish_parse(), salad_parse()]
        for val in menu:
            for elem in val:
                text = 'INSERT INTO Menu (type_p, name_p, description, price, image) VALUES (%s, %s, %s, %s, %s);'
                exec_tuple = (elem['type_p'], elem['name_p'], elem['description'], elem['price'], elem['image'])
                cursor.execute(text, exec_tuple)


cur.execute('DROP TABLE IF EXISTS Menu')
insert()