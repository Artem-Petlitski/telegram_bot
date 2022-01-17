############Клиентская часть#######################
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, kb_place
from aiogram.types import ReplyKeyboardRemove
from database import sqlite_db
from aiogram.types import *
from database import set_data, check, del_cart
YOOTOKEN = '381764678:TEST:32487'


# @dp.message_handler(commands=['start'])

async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Режимы работы', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")


# @dp.message_handler(commands=[ 'help', ])
async def command_help(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Приятного аппетита", reply_markup=ReplyKeyboardRemove())
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")


# @dp.message_handler(commands=["Режим_работы", ])
async def time_of_work(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Пн-Пт:с 9.00 до 18.00\nСб-Вс: с 10:00 до 16:00")
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")


# @dp.message_handler(commands=["Расположение"])
async def location(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Ул.Сурганова 47")
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")


@dp.message_handler(commands=["Доставка"])
async def dostavka(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Пицца будет доставлена через ~~  25 минут",request_location=True,
                               reply_markup=ReplyKeyboardRemove())
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")


@dp.message_handler(commands=["В пиццерии"])
async def v_piccerii(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "При получении пиццы предъявите ваш чек",
                               reply_markup=ReplyKeyboardRemove())
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")


async def buy_item(message: types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:{ret[2]}\nЦена{ret[-1]}')
        await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Добавить {ret[1]}', callback_data=f'buy {ret[1]}')))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('buy '))
async def buy_tovar(call: types.CallbackQuery):
    item = await sqlite_db.sql_read3(call.data.replace('buy ', ''))
    data = {
        'id': call.from_user.id,
        'product': item[1],
        'price': int(float(item[-1])),
    }

    await set_data(data)
    # await bot.send_invoice(chat_id=call.from_user.id, title=f"Покупка пиццы {item[1]}",
    #                        description=f"{item[2]}", payload="Monthsub", provider_token=YOOTOKEN,
    #                        currency='RUB', start_parameter='test_bot',
    #                        prices=[{'label': 'руб', 'amount': int(float(f' {item[-1]}') * 100)}])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    await del_cart(message.from_user.id)
    if message.successful_payment.invoice_payload == 'Monthsub':
        await message.answer("Вы успешно оплатили заказ", reply_markup=kb_place)




@dp.message_handler(text ="Оплатить")
async def patmetn(message: types.Message):
    # await sqlite_db.sql_read(message)
    await check(message.from_user.id)

@dp.message_handler(text="Удалить заказ")
async def del_order(message: types.Message):
    await message.answer("Заказ успешно удален")
    await del_cart(message.from_user.id)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(time_of_work, commands=["Режим_работы"])
    dp.register_message_handler(location, commands=['Расположение'])
    dp.register_message_handler(buy_item, commands=['Меню'])
    dp.register_message_handler(dostavka, commands=["Доставка"])
    dp.register_message_handler(v_piccerii, commands=["В_пиццерии"])
