from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
b1 = InlineKeyboardButton(text='1️⃣',callback_data='btn1')
b2 = InlineKeyboardButton(text='2️⃣',callback_data='btn2')
b3 = InlineKeyboardButton(text='3️⃣',callback_data='btn3')
b4 = InlineKeyboardButton(text='4️⃣',callback_data='btn4')
b5 = InlineKeyboardButton(text='5️⃣',callback_data='btn5')
b6 = InlineKeyboardButton(text='6️⃣',callback_data='btn6')
b7 = InlineKeyboardButton(text='7️⃣',callback_data='btn7')
b8 = InlineKeyboardButton(text='8️⃣',callback_data='btn8')
b9 = InlineKeyboardButton(text='9️⃣',callback_data='btn9')
b10 = InlineKeyboardButton(text='🔟',callback_data='btn10')


inkb = InlineKeyboardMarkup(row_width=2).add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10)