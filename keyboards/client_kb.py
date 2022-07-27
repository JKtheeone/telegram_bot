from aiogram.types import ReplyKeyboardMarkup , KeyboardButton #, ReplyKeyboardRemove

b1 = KeyboardButton('/My_TOP')
b2 = KeyboardButton('/Genres')
b3 = KeyboardButton('/Back')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b2 , b3)