import sqlite3


async def set_data(data: dict) -> None:
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT product, price
        FROM cart
        WHERE id = ?
    ''', (data['id'], ))
    result = cur.fetchone()
    if result:
        product, price = result
        product += f" {data['product']}"
        price += data['price']
        print(product, price)
        cur.execute('''
            UPDATE cart
            SET product = ?, price = ?
            WHERE id = ?
        ''', (product, price, data['id']))
    else:
        cur.execute('''
            INSERT INTO cart(id, product, price)
            VALUES(?, ?, ?)
        ''', (data['id'], data['product'], data['price']))
    conn.commit()
#
#
# conn = sqlite3.connect('../pizza_cool.db')
# cur = conn.cursor()
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS cart(
#         id INTEGER UNIQUE NOT NULL,
#         product TEXT NOT NULL,
#         price INTEGER NOT NULL)
# ''')
# conn.commit()