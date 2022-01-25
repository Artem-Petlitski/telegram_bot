############Клиентская часть#######################
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import kb_client, kb_place
from aiogram.types import ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from database import sqlite_db
from aiogram.types import *
from database import set_data, check, del_cart, set_order, history_order
from aiogram.utils.markdown import hlink

YOOTOKEN = '381764678:TEST:32487'


class FSMAdress(StatesGroup):
    adress = State()


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Меню команд', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")


@dp.message_handler(text='Главное меню')
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




@dp.message_handler(text="Поддержка")
async def help(message: types.Message):
    try:
        buttons = [
            types.InlineKeyboardButton(text="Vk", url="https://vk.com/pppet9"),
            types.InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/20_prosto_temka_01/")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer("Контакты разработчиков", reply_markup=keyboard)
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему! \nhttps://t.me/Pizza_ShefaBot")




async def category(message: types.Message):
    read = set(await sqlite_db.sql_category())
    kb_category = ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    tovar = []
    for ret in read:
        if ret[-1] not in tovar:
            if count == 0:
                kb_category.add(KeyboardButton(f"{ret[-1]}"))
                tovar.append(ret[-1])
                count += 1
            else:
                count = 0
                kb_category.insert(KeyboardButton(f"{ret[-1]}"))
                tovar.append(ret[-1])
    kb_category.add(KeyboardButton("Главное меню"))
    await bot.send_message(message.from_user.id, '*Категории:*', reply_markup=kb_category,
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(text=["Пиццы" ,'Напитки'])
async def buy_item(message: types.Message):
    read = await sqlite_db.sql_read2(message.text)
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:{ret[2]}\nЦена{ret[-2]}')
        await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Добавить {ret[1]}', callback_data=f'buy {ret[1]}')))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('buy '))
async def buy_tovar(call: types.CallbackQuery):
    item = await sqlite_db.sql_read3(call.data.replace('buy ', ''))
    data = {
        'id': call.from_user.id,
        'product': item[1],
        'price': int(float(item[-2])),
    }
    await bot.answer_callback_query(call.id, text="Товар добавлен в корзину")
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
    if message.successful_payment.invoice_payload == 'Monthsub':
        await message.answer("Вы успешно оплатили заказ")
        await FSMAdress.adress.set()
        await message.reply('Введите адрес доставки')


@dp.message_handler(content_types=['adress'], state=FSMAdress.adress)
async def adress(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['adress'] = message.text
    information = message.from_user
    print(information)
    await set_order(information, state)
    await del_cart(message.from_user.id)
    await state.finish()


@dp.message_handler(text="Оплатить")
async def patmetn(message: types.Message):
    # await sqlite_db.sql_read(message)
    await check(message.from_user.id)


@dp.message_handler(text="Удалить заказ")
async def del_order(message: types.Message):
    await message.answer("Заказ успешно удален")
    await del_cart(message.from_user.id)


# @dp.message_handler(text='История')
# async def order_history(message: types.Message):
#     await bot.send_message(message.from_user.id, "*Последние заказы*", parse_mode=ParseMode.MARKDOWN)
#     orders = await history_order(message.from_user.id)
#     print(orders)
#     for order in orders:
#         await bot.send_message(message.from_user.id,order)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(time_of_work, text="Режим_работы")
    dp.register_message_handler(location, text='Расположение')
    dp.register_message_handler(category, text='Меню')
    dp.register_message_handler(adress, state=FSMAdress.adress)
