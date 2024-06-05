import os
from slugify import slugify
from services import *
from flask import render_template, session, request, Flask, render_template_string, Response, redirect
from product import Product
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['UPLOAD_FOLDER'] = 'static/media/products'
app.config['SESSION_TYPE'] = 'filesystem'

stylesheet_source = os.path.abspath('static')


@app.route('/')
def index():
    with sq.Connection('flowershop_db.db') as con:
        cur = con.cursor()
        cats = cur.execute('SELECT name FROM Categories')
    return render_template('index.html', actual_flowers=get_actual_flowers(), cats=cats)


@app.route('/category/<category>')
def category(category):
    categories = get_actual_categories()
    with sq.Connection('flowershop_db.db') as con:
        cur = con.cursor()
        cats = cur.execute('SELECT name FROM Categories')
    return render_template('category.html', products=get_from_db_by_category(categories[category]),
                           title=category, cats=cats)


@app.route('/category/flowers/<category>')
def flowers_by_category(category):
    # return f'{get_from_db_by_flower_category(actual_categories[category])}'
    categories = get_actual_flower_categories()
    return render_template('category.html', products=get_from_db_by_flower_category(categories[category]),
                           title=category)

@app.route('/orders')
def orders():
    return render_template('orders.html', orders = get_orders())

@app.route('/cart')
def cart():
    products = []
    if 'cart' in session:
        products = session['cart'].items()
        print(products)
    res = sum(list(prod[1][5] * prod[1][7] for prod in products))
    # return f'Покупки: {products}'
    return render_template('cart.html', products=products, total_sum=res)

@app.route('/make-order', methods=['POST'])
def make_order():
    products = []
    if 'cart' in session:
        products = session['cart'].items()
        res = sum(list(prod[1][5] * prod[1][7] for prod in products))
        save_order(products, res, request.form['client_name'], request.form['phone'], datetime.datetime.now().strftime('%H:%M:%S / %d-%m-%Y'))
    
    clear()
    return redirect('/cart')

@app.route('/end-order/<int:id>')
def end_order(id):
    close_order(id)
    return redirect('/orders')

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


@app.route('/remove-cart/<int:id>')
def remove__from_cart_by_id(id):
    id = str(id)
    del session['cart'][id]
    session.modified = True
    return f'{session["cart"]}'


@app.route('/clear-cart')
def clear():
    session.pop('cart', None)
    return 'Deleted!'


@app.route('/decrease-count/<int:id>')
def decrease_count(id):
    id = str(id)
    session['cart'][id] = session['cart'][id][:7] + tuple([session['cart'][id][7] - 1])
    session.modified = True
    return ''


@app.route('/add-new-product', methods=['POST', "GET"])
def add_new_product():
    actual_categories = get_actual_categories()
    actual_flower_categories = get_actual_flower_categories()
    if request.method == 'POST':
        if len(list(request.values.items())) > 1:
            name = request.values['name']
            get_actual_categories()
            get_actual_flower_categories()
            category_id = actual_categories[request.values['category_list']]
            description = request.values['description']
            stock = int(request.values['stock'])
            is_actual = 1 if 'is_actual' in request.values and request.values['is_actual'] == 'on' else 0
            price = request.values['price']
            photo = request.files['image']
            flower_category = actual_flower_categories[request.values['flower_category']]
            slug = slugify(name)
            with sq.connect(DATABASE) as con:
                cur = con.cursor()
                photo_dir = os.path.join(app.config['UPLOAD_FOLDER'],
                                         f'{cur.execute("SELECT COUNT(last_insert_rowid()) FROM Flowers").fetchone()[0] + 1}_' + slug + '.png')
                photo.save(photo_dir)
                cur.execute(
                    f'INSERT INTO Flowers(name, category_id, description, stock, is_actual, price, flower_category_id, photo)'
                    f'VALUES (\'{name}\', {category_id}, \'{description}\', {stock}, {is_actual},{price}, {flower_category}, \'{photo_dir}\')')
                # cur.execute(f'UPDATE Flowers SET photo=\'{image_to_bytes(photo_dir)})/\')')
                cur.close()
                con.commit()
            # return f'<img src="data:image/png;base64,{image_to_bytes(photo_dir)}">'
            actual_categories = get_actual_categories()
            actual_flower_categories = get_actual_flower_categories()
            return render_template('add_products.html', categories=actual_categories.keys(),
                                   flower_categories=actual_flower_categories.keys())

        elif 'category_name' in request.values:
            status = ''
            cat_name = request.values['category_name'].capitalize()
            if cat_name in actual_categories:
                status = 'Категория уже существует \ Придумайте другое название'
            else:
                with sq.connect(DATABASE) as con:
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO Categories(name) VALUES ('{cat_name}')")
                    con.commit()
                    cur.close()
                status = 'Категория успешно добавлена'
            actual_categories = get_actual_categories()
            actual_flower_categories = get_actual_flower_categories()
            return render_template('add_products.html', categories=actual_categories.keys(),
                                   flower_categories=actual_flower_categories.keys(),
                                   category_request_status=f'{status}')

        elif 'flower_category_name' in request.values:
            status = ''
            cat_name = request.values['flower_category_name'].capitalize()
            if cat_name in actual_flower_categories:
                status = 'Разновидность уже существует \ Придумайте другое название'
            else:
                with sq.connect(DATABASE) as con:
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO FlowerCategory(name) VALUES ('{cat_name}')")
                    con.commit()
                    cur.close()
                status = 'Категория успешно добавлена'
            
            actual_categories = get_actual_categories()
            actual_flower_categories = get_actual_flower_categories()
            return render_template('add_products.html', categories=actual_categories.keys(),
                                   flower_categories=actual_flower_categories.keys(),
                                   flower_category_request_status=f'{status}')

    if request.method == 'GET':
        return render_template('add_products.html', categories=actual_categories.keys(),
                               flower_categories=actual_flower_categories.keys())

@app.route('/manage-products', methods=['GET', 'POST'])
def manage_product():
    if request.method == 'GET':
        with sq.Connection(DATABASE) as con:
            cur = con.cursor()
            products = list(Product(*args) for args in cur.execute('SELECT id, name, description, price, stock, photo FROM Flowers').fetchall())
        
        return render_template('manage_products.html', products=products)
@app.route('/remove-product/<int:id>')
def remove_product(id):
    id = int(id)
    with sq.Connection(DATABASE) as con:
        cur = con.cursor()
        cur.execute(f'DELETE FROM Flowers WHERE id={id}')
    
    return manage_product()

@app.route('/edit-price/<int:id>/<int:new_price>')
def edit_price(id, new_price):
    id = int(id)
    new_price = int(new_price)
    with sq.Connection(DATABASE) as con:
            cur = con.cursor()
            old_price = cur.execute(f'SELECT price FROM Flowers WHERE id={id}').fetchone()
            if old_price[0] != new_price:
                cur.execute(f'UPDATE Flowers SET price={new_price} WHERE id={id}')
    return manage_product()

@app.route('/admin-panel')
def admin_panel():
    actual_categories = get_actual_categories()
    actual_flower_categories = get_actual_flower_categories()
    return render_template('admin.html', categories=actual_categories.keys(),
                           flower_categories=actual_flower_categories.keys())


if __name__ == '__main__':
    app.run(debug=True)
