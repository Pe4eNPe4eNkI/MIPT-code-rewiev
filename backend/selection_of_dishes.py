from flask import Flask

from request import select_all_in_category

app = Flask(__name__)


@app.route('/selection/<category>/<prise>/<count>')
def selection(count: int, prise: int, category: str):
    return select_all_in_category(category)
