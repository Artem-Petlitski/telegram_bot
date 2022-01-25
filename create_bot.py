from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from sys import exit
from dotenv import load_dotenv
import os
load_dotenv('.env')
TOKEN = os.getenv("BOT_TOKEN")
YOOTOKEN = os.getenv("YOOMONEY")

storage = MemoryStorage()

# bot_token = getenv("BOT_TOKEN")
if not TOKEN:
    exit("Error:bot token not provided")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
