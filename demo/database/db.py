import pymysql
from pymysql import MySQLError



def db_connect():
    try:
        return pymysql.connect(
            host='localhost',
            user='root',
            password='R4321586y',
            database='day4_v1',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    except MySQLError as e:
        print('ошибка подключения к бд', e)
        return None


def check_login(username, password):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT users.user_id, users.full_name, roles.role_name
FROM users
JOIN roles ON roles.role_id = users.role_id
WHERE users.username = %s AND users.password = %s
""", (username, password))
            return cursor.fetchone()
    finally:
        db.close()


def all_categories():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT DISTINCT category AS category_name
FROM items
WHERE category IS NOT NULL AND category <> ''
ORDER BY category
""")
            return cursor.fetchall()
    finally:
        db.close()


def all_clients():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT users.user_id, users.full_name
FROM users
JOIN roles ON roles.role_id = users.role_id
WHERE roles.role_name = 'client'
ORDER BY users.full_name
""")
            return cursor.fetchall()
    finally:
        db.close()


def all_items():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
ORDER BY items.item_id
""")
            return cursor.fetchall()
    finally:
        db.close()


def one_item(item_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
WHERE items.item_id = %s
""", (item_id,))
            return cursor.fetchone()
    finally:
        db.close()


def items_by_category(category):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
WHERE items.category = %s
ORDER BY items.item_id
""", (category,))
            return cursor.fetchall()
    finally:
        db.close()


def search_items(text):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
WHERE items.item_name LIKE %s OR items.description LIKE %s
ORDER BY items.item_id
""", (f'%{text}%', f'%{text}%'))
            return cursor.fetchall()
    finally:
        db.close()


def items_sorted(sort_name, direction):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            if sort_name == 'Цена' and direction == 'ASC':
                cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
ORDER BY new_price ASC
""")
            elif sort_name == 'Цена' and direction == 'DESC':
                cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
ORDER BY new_price DESC
""")
            elif sort_name == 'Название' and direction == 'ASC':
                cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
ORDER BY items.item_name ASC
""")
            elif sort_name == 'Название' and direction == 'DESC':
                cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
ORDER BY items.item_name DESC
""")
            else:
                cursor.execute("""
SELECT items.item_id, items.item_name, items.description, items.price,
       items.image, items.category,
       discounts.discount_percent, discounts.date_end,
       ROUND(items.price * (100 - IFNULL(discounts.discount_percent, 0)) / 100, 2) AS new_price
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
ORDER BY items.item_id
""")
            return cursor.fetchall()
    finally:
        db.close()


def add_item(item_name, description, price, category, image):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
INSERT INTO items(item_name, description, price, category, image)
VALUES (%s, %s, %s, %s, %s)
""", (item_name, description, price, category, image))
            return cursor.lastrowid
    except Exception as e:
        print('ошибка добавления товара', e)
        return None
    finally:
        db.close()


def edit_item(item_id, item_name, description, price, category, image):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
UPDATE items
SET item_name = %s, description = %s, price = %s, category = %s, image = %s
WHERE item_id = %s
""", (item_name, description, price, category, image, item_id))
            return True
    except Exception as e:
        print('ошибка изменения товара', e)
        return False
    finally:
        db.close()


def delete_item(item_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE orders SET item_id = NULL WHERE item_id = %s", (item_id,))
            cursor.execute("DELETE FROM discounts WHERE item_id = %s", (item_id,))
            cursor.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
            return True
    except Exception as e:
        print('ошибка удаления товара', e)
        return False
    finally:
        db.close()


def save_discount(item_id, discount_percent, date_end):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM discounts WHERE item_id = %s", (item_id,))
            if int(discount_percent) > 0:
                cursor.execute("""
INSERT INTO discounts(item_id, discount_percent, date_start, date_end)
VALUES (%s, %s, CURDATE(), %s)
""", (item_id, discount_percent, date_end))
            return True
    except Exception as e:
        print('ошибка скидки', e)
        return False
    finally:
        db.close()


def all_orders():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT orders.order_id, orders.order_date, users.user_id,
       users.full_name AS client_name, orders.item_id,
       COALESCE(items.item_name, orders.item_name) AS item_name,
       orders.quantity, orders.delivery_type, orders.delivery_place,
       orders.total_amount, orders.status
FROM orders
JOIN users ON users.user_id = orders.user_id
LEFT JOIN items ON items.item_id = orders.item_id
ORDER BY orders.order_id DESC
""")
            return cursor.fetchall()
    finally:
        db.close()


def orders_by_user(user_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT orders.order_id, orders.order_date,
       COALESCE(items.item_name, orders.item_name) AS item_name,
       orders.quantity, orders.delivery_type, orders.delivery_place,
       orders.total_amount, orders.status
FROM orders
LEFT JOIN items ON items.item_id = orders.item_id
WHERE orders.user_id = %s
ORDER BY orders.order_id DESC
""", (user_id,))
            return cursor.fetchall()
    finally:
        db.close()


def one_order(order_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT order_id, user_id, item_id, quantity, delivery_type, delivery_place, status
FROM orders
WHERE order_id = %s
""", (order_id,))
            return cursor.fetchone()
    finally:
        db.close()


def add_order(user_id, item_id, quantity, delivery_type, delivery_place, status='Новый'):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT items.item_name, items.price, discounts.discount_percent
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
WHERE items.item_id = %s
""", (item_id,))
            item = cursor.fetchone()
            if item is None:
                return False
            price = float(item['price'])
            discount = item.get('discount_percent') or 0
            total = price * (100 - int(discount)) / 100 * int(quantity)
            cursor.execute("""
INSERT INTO orders(user_id, item_id, item_name, quantity, delivery_type,
                   delivery_place, total_amount, status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (user_id, item_id, item['item_name'], quantity, delivery_type,
      delivery_place, total, status))
            return True
    except Exception as e:
        print('ошибка добавления заказа', e)
        return False
    finally:
        db.close()


def edit_order(order_id, user_id, item_id, quantity, delivery_type, delivery_place, status):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT items.item_name, items.price, discounts.discount_percent
FROM items
LEFT JOIN discounts ON discounts.item_id = items.item_id
    AND CURDATE() BETWEEN discounts.date_start AND discounts.date_end
WHERE items.item_id = %s
""", (item_id,))
            item = cursor.fetchone()
            if item is None:
                return False
            price = float(item['price'])
            discount = item.get('discount_percent') or 0
            total = price * (100 - int(discount)) / 100 * int(quantity)
            cursor.execute("""
UPDATE orders
SET user_id = %s, item_id = %s, item_name = %s, quantity = %s,
    delivery_type = %s, delivery_place = %s, total_amount = %s, status = %s
WHERE order_id = %s
""", (user_id, item_id, item['item_name'], quantity, delivery_type,
      delivery_place, total, status, order_id))
            return True
    except Exception as e:
        print('ошибка изменения заказа', e)
        return False
    finally:
        db.close()


def delete_order(order_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
            return True
    except Exception as e:
        print('ошибка удаления заказа', e)
        return False
    finally:
        db.close()


def update_order_status(order_id, status):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (status, order_id))
            return True
    except Exception as e:
        print('ошибка статуса заказа', e)
        return False
    finally:
        db.close()
