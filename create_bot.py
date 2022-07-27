from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


bot = Bot(token = '1013129358:AAFdknauSEy1i8K7wMbkMAWaDj1ItGpYo-Q')
dp = Dispatcher(bot, storage=storage)