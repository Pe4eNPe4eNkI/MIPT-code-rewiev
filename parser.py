import urllib.request
from bs4 import BeautifulSoup


def parse():
    all_quotes = []
    for i in range(1, 3):
        request = urllib.request.urlopen(f'https://ilpatio.ru/category/pitstsa/?page={i}')
        html = request.read()
        bsObj = BeautifulSoup(html, 'html.parser')
        found_quotes = bsObj.find_all('div', {'class': 'product_list__item phx-15'})

        for found_quote in found_quotes:
            quote_name = found_quote.find('div', {'class': 'product_carousel__title'}).text
            quote_desc = found_quote.find('div', {'class': 'product_carousel__description'}).text
            quote_price = found_quote.find('div', {'class': 'product_carousel__price'}).text

            all_quotes.append({
                'name': ' '.join(quote_name.split()),
                'description': ' '.join(quote_desc.split()),
                'price': ' '.join(quote_price.split())
            })

    return all_quotes

