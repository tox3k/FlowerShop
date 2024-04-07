from flask import Flask, request
from ProductCard import ProductCard, ProductCard_Category, ProductCardList
import random

app = Flask(__name__)

cart = dict[int, ProductCard]
available_products = ProductCardList()

def get_rand_chrs_cnt(cnt):
    res = []
    for i in range(cnt):
        res.append(chr(random.randint(43, 70)))

    return res


def generateRandomProducts():
    for i in range(random.randint(10,20)):
        name = ''.join(get_rand_chrs_cnt(i))
        category = ProductCard_Category[random.randint(1, 4)]
        description = 'LOH'
        available_count = random.randint(15, 60)

        product = ProductCard(name=name, category=category, description=description, available_count=available_count)
        available_products.append(product)


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
