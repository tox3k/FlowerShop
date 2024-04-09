import os.path

from flask import *
import sqlite3 as sq

DATABASE = 'flowershop_db.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
actual_categories = {}
actual_flower_categories = {}
stylesheet_source = os.path.abspath('static')


@app.route('/')
def index():
    return render_template('index.html', actual_flowers=get_actual_flowers())


def get_actual_flowers():
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        res = cur.execute('SELECT * FROM Flowers '
                          'WHERE is_actual = 1').fetchall()
        cur.close()
        return res


@app.route('/add-cart/<int:id>')
def add_cart(id):
    str_id = str(id)
    if 'cart' in session and session['cart'] is not None:
        if str_id in session['cart']:
            session['cart'][str_id] = session['cart'][str_id][:7] + tuple([session['cart'][str_id][7] + 1])
        else:
            session['cart'][str_id] = get_from_db_by_id(str_id)[1:] + tuple([1])


    else:
        session['cart'] = {str_id: get_from_db_by_id(str_id)[1:] + tuple([1])}
    session.modified = True
    return f'{session["cart"].items()} {str_id in session["cart"]} test'

@app.route('/clear-cart')
def clear():
    session.pop('cart', None)
    return 'Deleted!'

@app.route('/cart')
def cart():
    products = []
    if 'cart' in session:
        products = session['cart'].items()

    # return f'Покупки: {products}'
    return render_template('cart.html', products=products)


@app.route('/category/flowers/<category>')
def flowers_by_category(category):
    get_actual_flower_categories()
    # return f'{get_from_db_by_flower_category(actual_categories[category])}'
    return render_template('category.html', products=get_from_db_by_flower_category(actual_flower_categories[category]), title=category)

@app.route('/category/<category>')
def category(category):
    get_actual_categories()
    return render_template('category.html', products=get_from_db_by_category(actual_categories[category]))

def get_actual_categories():
    categories = []
    global actual_categories
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        categories = cur.execute('SELECT * FROM Categories').fetchall()
        cur.close()
    actual_categories = {}
    for cat in categories:
        actual_categories[cat[1]] = cat[0]

def get_actual_flower_categories():
    categories = []
    global actual_flower_categories
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        categories = cur.execute('SELECT * FROM FlowerCategory').fetchall()
        cur.close()
    actual_flower_categories = {}
    for cat in categories:
        actual_flower_categories[cat[1]] = cat[0]

def get_from_db_by_flower_category(category_id):
    '''
    Получение цветов из базы данных по категории
    :param category_id: id категории можно получить из глобальной переменной actual_categories (ключ - имя категории)
    :return:
    '''
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        flowers = cur.execute(f'SELECT * FROM Flowers WHERE flower_category_id = {category_id}').fetchall()
        cur.close()
        return flowers

def get_from_db_by_category(category_id):
    '''
    Получение цветов из базы данных по категории
    :param category_id: id категории можно получить из глобальной переменной actual_categories (ключ - имя категории)
    :return:
    '''
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        flowers = cur.execute(f'SELECT * FROM Flowers WHERE category_id = {category_id}').fetchall()
        cur.close()
        return flowers

def get_from_db_by_id(id) -> tuple:
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        res = cur.execute(f'SELECT * FROM Flowers WHERE id = {id}').fetchone()
        return res


if __name__ == '__main__':
    app.run(debug=True)
