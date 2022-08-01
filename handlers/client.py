from ast import Lambda
from aiogram import Dispatcher, types
from create_bot import dp,bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from data_base import sqlite_db
from keyboards import inline
from aiogram.dispatcher.filters import Text


#@dp.message_handler(commands=['start','help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id,'NOW YOU ARE GONE',reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Если тут когда то будет канал а непросто бот то ошибка связанная с отправлением сообщений в личку вот ссылка на бота: \nhttps://t.me/PickyOneBot')

#@dp.message_handler(commands=['My_TOP'])
#async def command_top(message : types.Message):
        #await bot.send_message(message.from_user.id,'MYTOPLETITGOBROOO0')

#@dp.message_handler(commands=['Genres'])
async def command_genres(message : types.Message):
        #await bot.send_message(message.from_user.id,'GENRES THAT I KNOW')
        await message.answer(text='Выберите жанр и нажмите на соответствующую кнопку' ,reply_markup=inline.inkbg)

#@dp.message_handler(commands=['Back'])
async def command_all(message : types.Message):
        await bot.send_message(message.from_user.id,text=sqlite_db.sql_all())


#@dp.message_handler(commands=['My_TOP'])
async def command_top(message : types.Message):
        #await sqlite_db.sql_read(message)  
        await message.answer(sqlite_db.sql_readx(),reply_markup=inline.inkb)

#@dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))         
async def process_callback_kbbtn(callback_query: types.CallbackQuery):
        code = callback_query.data[-1]
        if code.isdigit():
                code = int(code)
    #if code == 1:
        #await sqlite_db.sql_show_variant(callback_query)
        #print(sqlite_db.sql_top())
        await sqlite_db.sql_show_variant(callback_query.from_user.id,code)
        await bot.answer_callback_query(callback_query.id)

async def process_callback_kbbtng(callback_query : types.CallbackQuery):
        code = callback_query.data[-1]
        if code.isdigit():
                code = int(code)
        await sqlite_db.sql_genre_filter(callback_query.from_user.id,code)
        await bot.answer_callback_query(callback_query.id)

#@dp.message_handler()
#async def empty(message : types.Message):
        #await message.answer('Такой команды не существует')
        #await message.delete()

async def command_test1(message : types.Message):
    data = await sqlite_db.sql_get()
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for i, film_index in enumerate(data['indices']):
        b = InlineKeyboardButton(text=f'{i + 1}',callback_data=f'btn{film_index}')
        inline_kb.add(b)
    
    await message.answer(data['message'], reply_markup=inline_kb)

#@dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btntest1'))         
async def process_callback_kbbtn(callback_query: types.CallbackQuery):
    code = callback_query.data.strip('btntest1')
    if code.isdigit():
        code = int(code)
        await sqlite_db.sql_show_variant(callback_query.from_user.id, code)
    else:
        # можно добавить листание страниц
        pass

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start,commands=['start','help'])
    #dp.register_message_handler(command_top,commands=['My_TOP'])
    dp.register_message_handler(command_top,Text(equals = ['top','🔟','top🔟'],ignore_case = True))
    dp.register_message_handler(command_genres,commands=['Genres'])
    dp.register_message_handler(command_all,commands=['All'])
    dp.register_message_handler(command_test1,commands=['test1'])
    dp.register_callback_query_handler(process_callback_kbbtn,lambda c: c.data and c.data.startswith('btn'))
    dp.register_callback_query_handler(process_callback_kbbtng,lambda c: c.data and c.data.startswith('gbtn'))
    #dp.register_message_handler(empty)