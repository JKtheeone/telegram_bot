from aiogram import Dispatcher, types
from create_bot import dp,bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
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

#@dp.message_handler(commands=['Genres'])
async def command_genres(message : types.Message):
        #await bot.send_message(message.from_user.id,'GENRES THAT I KNOW')`test`
        await message.answer(text='*Выберите жанр и нажмите на соответствующую кнопку:*' ,reply_markup=inline.inkbg,parse_mode='Markdown')

async def command_all(message : types.Message):
        #await bot.send_message(message.from_user.id,text=sqlite_db.sql_all(),reply_markup=inline.in1)
        #await sqlite_db.send_film_page(message)
        await sqlite_db.sql_filter(message,code = 0,page = 1,sql_query= 'all')
#@dp.message_handler(commands=['My_TOP'])
async def command_top(message : types.Message):
        #await sqlite_db.sql_read(message)  
        await sqlite_db.sql_show_top(message.from_user.id)

async def command_inrate_order(message : types.Message):
        await bot.send_message(message.from_user.id,text='*Выберите оценку*',reply_markup=inline.inkbr,parse_mode='Markdown')
        #await sqlite_db.send_inrate_order(message)

async def process_callback_rate(callback_query : types.CallbackQuery):
        code = callback_query.data.split('#')[1]
        if code.isdigit():
                code = int(code)
        await sqlite_db.sql_filter(callback_query.message, code, 1, 'rate')
        await bot.answer_callback_query(callback_query.id)

#@dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))         
async def process_callback_kbbtn(callback_query: types.CallbackQuery):
        code = callback_query.data.split('#')[1]
        if code.isdigit():
                code = int(code)
        await sqlite_db.sql_show_top(callback_query.from_user.id,code)
        await bot.answer_callback_query(callback_query.id)

async def process_callback_kbbtng(callback_query : types.CallbackQuery):
        code = callback_query.data.split('#')[1]
        if code.isdigit():
                code = int(code)
        await sqlite_db.sql_filter(callback_query.message, code, 1, 'genre')
        await bot.answer_callback_query(callback_query.id)

async def process_callback_pagination(callback_query : types.CallbackQuery):
        film = int(callback_query.data.split('#')[1])
        await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
        await sqlite_db.send_film_page(callback_query.message,film)
        
async def show_with_command(message : types.Message):
        code = int(message.text.split('f')[1])
        await sqlite_db.sql_show_variant(message.from_user.id,code)

async def command_info(message : types.Message):
        await bot.send_message(message.from_user.id,text='_Жалобы,предложения и вопросы писать сюда -_ @jktherealone',parse_mode='Markdown')

async def proccess_callback_more(callback_query : types.CallbackQuery):
        await sqlite_db.send_film_page(callback_query.message)
        await bot.answer_callback_query(callback_query.id)

async def proccess_callback_pages(callback_query : types.CallbackQuery):
        page = int(callback_query.data.split('#')[1])
        await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
        await sqlite_db.pages(callback_query.message,page)

async def proccess_callback_showfilmpage(callback_query : types.CallbackQuery):
        film = int(callback_query.data.split('f')[1])
        await sqlite_db.sql_show_variant(callback_query.from_user.id,film)
        await bot.answer_callback_query(callback_query.id)

async def proccess_callback_pagesfilter(callback_query : types.CallbackQuery):
        data = callback_query.data.split('#')[1].split(':')
        page, code = map(int, data[:2])
        sql_query = data[2]
        await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
        await sqlite_db.sql_filter(chatid=callback_query.message, code=code, page=page, sql_query=sql_query)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start,commands=['start','help'])
    dp.register_message_handler(command_top,Text(equals = ['top','🔟','top🔟'],ignore_case = True))
    dp.register_message_handler(command_genres,Text(equals = ['Жанры','🔄','Жанры🔄'],ignore_case = True))
    dp.register_message_handler(command_all,Text(equals = ['Все фильмы','Фильмы','Все фильмы🎦','🎦'],ignore_case = True))
    dp.register_message_handler(command_inrate_order,Text(equals = ['По рейтингу','Фильтр по рейтингу🔢','🔢'],ignore_case = True))
    dp.register_message_handler(show_with_command,lambda c: c.text.startswith('/f'))
    dp.register_callback_query_handler(process_callback_kbbtn,lambda c: c.data and c.data.startswith('btn'))
    dp.register_callback_query_handler(process_callback_kbbtng,lambda c: c.data and c.data.startswith('gbtn'))
    dp.register_callback_query_handler(process_callback_pagination,lambda c: c.data and c.data.startswith('film'))
    dp.register_callback_query_handler(proccess_callback_more,lambda c: c.data and c.data.startswith('more'))
    dp.register_callback_query_handler(proccess_callback_pages,lambda c: c.data and c.data.startswith('page'))
    dp.register_callback_query_handler(process_callback_rate,lambda c: c.data and c.data.startswith('rate'))
    dp.register_callback_query_handler(proccess_callback_showfilmpage,lambda c: c.data and c.data.startswith('/f'))
    dp.register_callback_query_handler(proccess_callback_pagesfilter,lambda c: c.data and c.data.startswith('forfilter'))
    dp.register_message_handler(command_info,commands=['links'])
    #dp.register_message_handler(empty)