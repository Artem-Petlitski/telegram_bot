from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

workmode = KeyboardButton("/Режим_работы")
location = KeyboardButton("/Расположение")
menu = KeyboardButton("/Меню")
order = KeyboardButton("Оплатить")
# b4 = KeyboardButton("/Пополнение счета")
in_pizzeria = KeyboardButton("/В_пиццерии")
dostavka = KeyboardButton("/Доставка")
back_order = KeyboardButton("Удалить заказ")
help_contact = KeyboardButton("Поддержка")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_place = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_place.add(in_pizzeria).insert(dostavka)
kb_client.add(workmode).insert(location).add(menu).insert(order).add(back_order).add(help_contact)
