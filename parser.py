import urllib.request
from bs4 import BeautifulSoup


def parse(all_quotes, found_quotes, bsObj):
    category = bsObj.find('h1', {'class': 'category-name ptx-10'}).text
    for found_quote in found_quotes:
        quote_name = found_quote.find('div', {'class': 'product_carousel__title'}).text
        quote_desc = found_quote.find('div', {'class': 'product_carousel__description'}).text
        quote_price = found_quote.find('div', {'class': 'product_carousel__price'}).text

        all_quotes.append({
            'type': category,
            'name': ' '.join(quote_name.split()),
            'description': ' '.join(quote_desc.split()),
            'price': ' '.join(quote_price.split())
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
