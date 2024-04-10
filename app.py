import os.path
import base64
import threading

from flask import *
import sqlite3 as sq

DATABASE = 'flowershop_db.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['UPLOAD_FOLDER'] = os.path.abspath('static/media/products')
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


@app.route('/remove-cart/<int:id>')
def remove__from_cart_by_id(id):
    id = str(id)
    del session['cart'][id]
    session.modified = True
    return f'{session["cart"]}'


@app.route('/cart')
def cart():
    products = []
    if 'cart' in session:
        products = session['cart'].items()
    res = sum(list(prod[1][5] * prod[1][7] for prod in products))
    # return f'Покупки: {products}'
    return render_template('cart.html', products=products, total_sum=res)


@app.route('/decrease-count/<int:id>')
def decrease_count(id):
    id = str(id)
    session['cart'][id] = session['cart'][id][:7] + tuple([session['cart'][id][7] - 1])
    session.modified = True
    return ''


@app.route('/category/flowers/<category>')
def flowers_by_category(category):
    get_actual_flower_categories()
    # return f'{get_from_db_by_flower_category(actual_categories[category])}'
    return render_template('category.html', products=get_from_db_by_flower_category(actual_flower_categories[category]),
                           title=category)


@app.route('/category/<category>')
def category(category):
    get_actual_categories()
    return render_template('category.html', products=get_from_db_by_category(actual_categories[category]),
                           title=category)


@app.route('/admin-panel')
def admin_panel():
    get_actual_categories()
    get_actual_flower_categories()
    return render_template('admin.html', categories=actual_categories.keys(),
                           flower_categories=actual_flower_categories.keys())


@app.route('/add-new-product', methods=['POST'])
def add_new_product():
    name = request.values['name']
    get_actual_categories()
    get_actual_flower_categories()
    category_id = actual_categories[request.values['category_list']]
    description = request.values['description']
    stock = int(request.values['stock'])
    is_actual = 1 if request.values['is_actual'] == 'on' else 0
    price = request.values['price']
    photo = request.files['image']
    photo_dir = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
    photo.save(photo_dir)
    flower_category = actual_flower_categories[request.values['flower_category']]

    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO Flowers(name, category_id, description, stock, is_actual, price, flower_category_id, photo)'
                    f'VALUES (\'{name}\', {category_id}, \'{description}\', {stock}, {is_actual},{price}, {flower_category}, \'{image_to_bytes(photo_dir)}\')')
        # cur.execute(f'UPDATE Flowers SET photo=\'{image_to_bytes(photo_dir)})/\')')
        cur.close()
        con.commit()
    os.remove(photo_dir)
    # return f'<img src="data:image/png;base64,{image_to_bytes(photo_dir)}">'
    return admin_panel()


def image_to_bytes(image_dir):
    with (open(image_dir, 'rb') as f):
        data = base64.b64encode(f.read())
        return str(data)[2:-1]


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
