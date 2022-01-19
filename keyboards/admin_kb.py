from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

button_load = KeyboardButton("/Загрузить")
button_delete = KeyboardButton("/Удалить")
button_done_order = KeyboardButton("Готовый заказ")

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).insert(button_delete).add(button_done_order)
