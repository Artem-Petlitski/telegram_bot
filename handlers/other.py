from aiogram import types,Dispatcher
import string, json
from create_bot import dp, bot


# @dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")}.intersection(
            set(json.load(open('error_words.json')))) != set():
        await message.answer("Маты запрещены")
        await message.delete()

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
