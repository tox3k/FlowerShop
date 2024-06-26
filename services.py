import sqlite3 as sq
import order
import product
DATABASE = 'flowershop_db.db'

def get_actual_flowers():
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        res = cur.execute('SELECT * FROM Flowers '
                          'WHERE is_actual = 1').fetchall()
        cur.close()
        return res


def get_actual_categories():
    actual_categories = {}
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        categories = cur.execute('SELECT * FROM Categories').fetchall()
        cur.close()
    for cat in categories:
        actual_categories[cat[1]] = cat[0]
    return actual_categories


def get_actual_flower_categories():
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        categories = cur.execute('SELECT * FROM FlowerCategory').fetchall()
        cur.close()
    actual_flower_categories = {}


    for cat in categories:
        actual_flower_categories[cat[1]] = cat[0]

    return actual_flower_categories


def get_from_db_by_flower_category(category_id) -> list:
    '''
    Получение цветов из базы данных по категории
    :param category_id: id категории можно получить из глобальной переменной actual_categories (ключ - имя категории)
    :return: Список словарей с данными из БД
    '''
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        flowers = cur.execute(f'SELECT * FROM Flowers WHERE flower_category_id = {category_id}').fetchall()
        cur.close()
        return flowers


def get_from_db_by_category(category_id):
    '''
    Получение товаров из базы данных по категории
    :param category_id: id категории можно получить из глобальной переменной actual_categories (ключ - имя категории)
    :return:
    '''
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        flowers = cur.execute(f'SELECT * FROM Flowers WHERE category_id = {category_id}').fetchall()
        cur.close()
        return flowers

def save_order(products, price, client, phone, timestamp):
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO Orders(price, client_name, timestamp, phone) VALUES(\'{price}\', \'{client}\', \'{timestamp}\', \'{phone}\')')
        order_id = cur.execute(f'SELECT order_id FROM Orders WHERE price=\'{price}\' AND client_name=\'{client}\' AND timestamp=\'{timestamp}\' AND phone=\'{phone}\'').fetchone()[0]
        for p in products:
            cur.execute(f'INSERT INTO Orders_additional VALUES(\'{order_id}\', \'{p[0]}\', \'{p[1][0]}\', \'{p[1][7]}\')')
        cur.close()
        
        

def get_from_db_by_id(id) -> tuple:
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        res = cur.execute(f'SELECT * FROM Flowers WHERE id = {id}').fetchone()
        return res

def get_orders():
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        r = cur.execute(f'SELECT * FROM Orders WHERE performed=\'0\'')
        orders: list[order.Order] = []
        for o in r:
            ord = order.Order(o[0], o[2], o[5], o[1], o[3], [])
            orders.append(ord)
        
        for o in orders:
            products = cur.execute(f'SELECT product_id, product_name, product_count FROM Orders_additional WHERE order_id={o.id}').fetchall()
            print(products)
            for p in products:
                o.products.append(product.Product(id=p[0], name=p[1], count=p[2]))
        
        return orders

def close_order(id):
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(f'UPDATE Orders SET performed=\'1\' WHERE order_id=\'{id}\'')