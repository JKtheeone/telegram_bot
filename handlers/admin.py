from datetime import date
from typing import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


from data_base.sqlite_db import sql_add_command

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    genre = State()
    desription = State()
    date = State()
    rate = State()

#Получить ID текущего модератора
#@dp.message_handler(commands=['moderator'], is_chat_admin = True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Вот ю вонт гандон', reply_markup = admin_kb.button_case_admin)
    await message.delete()
#Начало диалога загрузки нового пункта меню
#@dp.message_handler(commands = 'Загрузить',state = None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

#Выход из состояний
#@dp.message_handler(state = "*", commands='отмена')
#@dp.message_handler(Text(equals = 'отмена', ignore_case = True),state ="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

#Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types =['photo'], state = FSMAdmin.photo)
async def load_photo(message : types.Message , state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи название')

#Второй ответ
#@dp.message_handler(state = FSMAdmin.name)
async def load_name(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи жанр фильма')

async def load_genre(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['genre'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание фильма')
#Ловим третий ответ
#@dp.message_handler(state = FSMAdmin.desription)
async def load_description(message: types.Message , state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введи дату')
#Ловим четвертый ответ
#@dp.message_handler(state = FSMAdmin.date)
async def load_date(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['date'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введи рейтинг')
#Ластовый ответ и использование полученных данных
#@dp.message_handler(state = FSMAdmin.rate)
async def load_rate(message: types.Message, state : FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['rate'] = int(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()

@dp.message_handler(commands='Удалить')
async def delete_item(message : types.Message):
    if message.from_user.id == ID:
        read = sqlite_db.sql_read2()
        for x in read:
            await bot.send_photo(message.from_user.id,x[1],f'{x[2]}\nЖанр: {x[3]}\nОписание: {x[4]}\nДата создания: {x[5]}\nРейтинг: {x[-1]}')
            await bot.send_message(message.from_user.id,text='^',reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {x[2]}',callback_data=f'del {x[2]}')))

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query : types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} удалена',show_alert=True)

#Регистрируем хендлеры
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state = None)
    dp.register_message_handler(cancel_handler,state = "*", commands='отмена')
    dp.register_message_handler(cancel_handler,Text(equals = 'отмена', ignore_case = True),state ="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state = FSMAdmin.photo)
    dp.register_message_handler(load_name, state = FSMAdmin.name)
    dp.register_message_handler(load_genre, state=FSMAdmin.genre)
    dp.register_message_handler(load_description,  state = FSMAdmin.desription)
    dp.register_message_handler(load_date,state = FSMAdmin.date)
    dp.register_message_handler(load_rate, state = FSMAdmin.rate)
    dp.register_message_handler(make_changes_command,commands=['moderator'], is_chat_admin = True)
    #dp.register_message_handler(delete_item,commands='Удалить')
    #dp.register_callback_query_handler(del_callback_run)
