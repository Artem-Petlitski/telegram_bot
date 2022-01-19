import sqlite3 as sq
from create_bot import bot
from aiogram.types.labeled_price import LabeledPrice


async def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print("Database connected")
    base.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT,name TEXT PRIMARY KEY,description TEXT,price INTEGER )")
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * from menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:{ret[2]}\nЦена {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_read3(data):
    return cur.execute('SELECT * FROM menu WHERE name == ?', (data,)).fetchall()[0]


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()


async def check(user_id: int) -> None:
    conn = sq.connect('pizza_cool.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT price
        FROM cart
        WHERE id = ?
    ''', (user_id,))
    price = cur.fetchone()
    price = price[0] if price else False
    YOOTOKEN = '381764678:TEST:32487'
    if price:
        await bot.send_invoice(chat_id=user_id, title="Оплата заказа",
                               description='Пиццерия', payload="Monthsub", provider_token=YOOTOKEN,
                               currency='RUB', start_parameter='test_bot',
                               prices=[{'label': 'руб', 'amount': int(float(f' {price}') * 100)}])
    else:
        await bot.send_message(user_id, 'Извините, ваша корзина пуста')


# id product price adress is_done

async def set_data(data: dict) -> None:
    conn = sq.connect('pizza_cool.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT product, price
        FROM cart
        WHERE id = ?
    ''', (data['id'],))
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


async def del_cart(user_id: int) -> None:
    conn = sq.connect('pizza_cool.db')
    cur = conn.cursor()
    cur.execute('''
            DELETE FROM cart WHERE id = ?
        ''', (user_id,))
    conn.commit()


async def set_order(place: dict) -> None:
    conn = sq.connect('pizza_cool.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT product
        FROM cart
        WHERE id = ?
    ''', (place['id'],))
    result = cur.fetchone()
    if result:
        product = result
        print(product)
        cur.execute('''
            INSERT INTO orders(first_name,last_name,user_id, product,adress,is_done )
            VALUES(?, ?, ?,?,?,?)
        ''', (place['first_name'], place['last_name'], place['id'], str(product), 'ads', False))
    conn.commit()


# conn = sqlite3.connect('../../db.db')
# cur = conn.cursor()
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS cart(
#         id INTEGER UNIQUE NOT NULL,
#         product TEXT NOT NULL,
#         price INTEGER NOT NULL)
# ''')
# conn.commit()

# conn = sq.connect('../pizza_cool.db')
# cur = conn.cursor()
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS orders(
#         id INTEGER PRIMARY KEY,
#         first_name TEXT NOT NULL,
#         last_name TEXT NOT NULL,
#         user_id INTEGER,
#         product TEXT NOT NULL,
#         adress TEXT NOT NULL,
#         is_done BOOL)
# ''')
# conn.commit()
