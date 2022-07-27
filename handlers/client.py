import imp
from aiogram import Dispatcher, types
from create_bot import dp,bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from keyboards import inline

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
        await bot.send_message(message.from_user.id,'GENRES THAT I KNOW')

#@dp.message_handler(commands=['Back'])
async def command_back(message : types.Message):
        await bot.send_message(message.from_user.id,'I HOPE U ARE BACK',reply_markup=ReplyKeyboardRemove())


#@dp.message_handler(commands=['My_TOP'])
async def command_top(message : types.Message):
        #await sqlite_db.sql_read(message)  
        await message.answer(sqlite_db.sql_readx(),reply_markup=inline.inkb)

#@dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))         
async def process_callback_kbbtn(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
        #await sqlite_db.sql_show_variant(callback_query)
        await sqlite_db.sql_show_variant(callback_query.from_user.id)
        await bot.answer_callback_query(callback_query.id)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start,commands=['start','help'])
    dp.register_message_handler(command_top,commands=['My_TOP'])
    dp.register_message_handler(command_genres,commands=['Genres'])
    dp.register_message_handler(command_back,commands=['Back'])
    dp.register_callback_query_handler(process_callback_kbbtn)