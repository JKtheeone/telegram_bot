from aiogram.types import ReplyKeyboardMarkup , KeyboardButton #, ReplyKeyboardRemove

b1 = KeyboardButton('TOP🔟')
b2 = KeyboardButton('Жанры🔄')
b3 = KeyboardButton('Все фильмы🎦')
b4 = KeyboardButton('Фильтр по рейтингу🔢')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b2 , b3).add(b4)