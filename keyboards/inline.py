from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

b1 = InlineKeyboardButton(text='1️⃣',callback_data='btn#1')
b2 = InlineKeyboardButton(text='2️⃣',callback_data='btn#2')
b3 = InlineKeyboardButton(text='3️⃣',callback_data='btn#3')
b4 = InlineKeyboardButton(text='4️⃣',callback_data='btn#4')
b5 = InlineKeyboardButton(text='5️⃣',callback_data='btn#5')
b6 = InlineKeyboardButton(text='6️⃣',callback_data='btn#6')
b7 = InlineKeyboardButton(text='7️⃣',callback_data='btn#7')
b8 = InlineKeyboardButton(text='8️⃣',callback_data='btn#8')
b9 = InlineKeyboardButton(text='9️⃣',callback_data='btn#9')
b10 = InlineKeyboardButton(text='🔟',callback_data='btn#10')


inkb = InlineKeyboardMarkup(row_width=2).add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10)


bg1 = InlineKeyboardButton(text='Аниме',callback_data='gbtn#1')
bg2 = InlineKeyboardButton(text='Биография',callback_data='gbtn#2')
bg3 = InlineKeyboardButton(text='Боевик',callback_data='gbtn#3')
bg4 = InlineKeyboardButton(text='Вестерн',callback_data='gbtn#4')
bg5 = InlineKeyboardButton(text='Военный',callback_data='gbtn#5')
bg6 = InlineKeyboardButton(text='Детектив',callback_data='gbtn#6')
bg7 = InlineKeyboardButton(text='Документальные',callback_data='gbtn#7')
bg8 = InlineKeyboardButton(text='Драма',callback_data='gbtn#8')
bg9 = InlineKeyboardButton(text='Исторические',callback_data='gbtn#9')
bg10 = InlineKeyboardButton(text='Комедия',callback_data='gbtn#10')
bg11 = InlineKeyboardButton(text='Криминал',callback_data='gbtn#11')
bg12 = InlineKeyboardButton(text='Мультфильмы',callback_data='gbtn#12')
bg13 = InlineKeyboardButton(text='Приключения',callback_data='gbtn#13')
bg14 = InlineKeyboardButton(text='Спортивные',callback_data='gbtn#14')
bg15 = InlineKeyboardButton(text='Триллер',callback_data='gbtn#15')
bg16 = InlineKeyboardButton(text='Ужасы',callback_data='gbtn#16')
bg17 = InlineKeyboardButton(text='Фантастика',callback_data='gbtn#17')
bg18 = InlineKeyboardButton(text='Фэнтези',callback_data='gbtn#18')

inkbg = InlineKeyboardMarkup(row_width=3).add(bg1,bg2,bg3,bg4,bg5,bg6,bg7,bg8,bg9,bg10,bg11,bg12,bg13,bg14,bg15,bg16,bg17,bg18)

bm = InlineKeyboardButton(text='Подробно',callback_data='more')

in1 = InlineKeyboardMarkup(row_width=1).add(bm)

r1 = InlineKeyboardButton(text='1️⃣',callback_data='rate#1')
r2 = InlineKeyboardButton(text='2️⃣',callback_data='rate#2')
r3 = InlineKeyboardButton(text='3️⃣',callback_data='rate#3')
r4 = InlineKeyboardButton(text='4️⃣',callback_data='rate#4')
r5 = InlineKeyboardButton(text='5️⃣',callback_data='rate#5')
r6 = InlineKeyboardButton(text='6️⃣',callback_data='rate#6')
r7 = InlineKeyboardButton(text='7️⃣',callback_data='rate#7')
r8 = InlineKeyboardButton(text='8️⃣',callback_data='rate#8')
r9 = InlineKeyboardButton(text='9️⃣',callback_data='rate#9')
r10 = InlineKeyboardButton(text='🔟',callback_data='rate#10')

inkbr = InlineKeyboardMarkup(row_width=2).add(r1,r2,r3,r4,r5,r6,r7,r8,r9,r10)

