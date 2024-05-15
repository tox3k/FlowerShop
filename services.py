import sqlite3 as sq

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


def get_from_db_by_id(id) -> tuple:
    with sq.connect(DATABASE) as con:
        cur = con.cursor()
        res = cur.execute(f'SELECT * FROM Flowers WHERE id = {id}').fetchone()
        return res