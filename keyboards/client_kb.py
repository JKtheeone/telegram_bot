from aiogram.types import ReplyKeyboardMarkup , KeyboardButton #, ReplyKeyboardRemove

#b1 = KeyboardButton('/My_TOP')
b1 = KeyboardButton('TOP🔟')
b2 = KeyboardButton('/Genres')
b3 = KeyboardButton('/All')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b2 , b3)