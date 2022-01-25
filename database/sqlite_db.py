import sqlite3 as sq
from create_bot import bot, YOOTOKEN
from aiogram.types.labeled_price import LabeledPrice



async def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print("Database connected")
    base.execute("CREATE TABLE IF NOT EXISTS Menu(img TEXT,name TEXT PRIMARY KEY,description TEXT,price INTEGER,category TEXT)")
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO Menu VALUES(?,?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * from Menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:{ret[2]}\nЦена {ret[-1]}')



async def sql_category():
    return cur.execute('SELECT * FROM Menu').fetchall()

async def sql_read2(category):
    return cur.execute('SELECT * FROM menu WHERE category == ?',(category,)).fetchall()


async def sql_read3(data):
    return cur.execute('SELECT * FROM Menu WHERE name == ?', (data,)).fetchall()[0]


async def sql_delete_command(data):
    cur.execute('DELETE FROM Menu WHERE name == ?', (data,))
    base.commit()

async def history_order(user_id):
    conn = sq.connect('pizza_cool.db')
    print(user_id)
    cur = conn.cursor()
    return cur.execute('''
            SELECT product FROM orders WHERE user_id = ? 
        ''', (user_id,)).fetchmany(3)



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


async def set_order(place: dict,state) -> None:
    conn = sq.connect('pizza_cool.db')
    cur = conn.cursor()
    async with state.proxy() as data:
        cur.execute('''
            SELECT product
            FROM cart
            WHERE id = ?
        ''', (place['id'],))
        result = cur.fetchone()
        if result:
            product = result
            print(product)
            # print(data['adress'])
            cur.execute('''
                INSERT INTO orders(first_name,user_id, product,adress,is_done)
                VALUES(?,  ?,?,?,?)
            ''', (place['first_name'], place['id'], str(product), data['adress'], False))
        conn.commit()

async def sql_done_order(state):
    conn = sq.connect('pizza_cool.db')
    cur = conn.cursor()
    async with state.proxy() as data:
        print(data['number_order'])
        cur.execute('''
                UPDATE orders
                SET is_done =  TRUE
                WHERE id = ?
            ''', (data['number_order']))
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
#         user_id INTEGER,
#         product TEXT NOT NULL,
#         adress TEXT NOT NULL,
#         is_done BOOL)
# ''')
# conn.commit()
