from flask import Flask, request
from flaskext.mysql import MySQL
from ProductCard import ProductCard, ProductCard_Category, ProductCardList
import random

mysql = MySQL()
app = Flask(__name__)
mysql.init_app(app)
cursor = mysql.get_db().cursor()

@app.route('/')
def index():
    generateRandomProducts()
    available = (product.name for product in available_products.items())
    return available

@app.route('/add-cart/<int:id>')
def add_cart(id):

    pass


if __name__ == '__main__':
    app.run(debug=True)
