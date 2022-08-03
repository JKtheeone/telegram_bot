#from aiogram.utils.callback_data import CallbackData
import sqlite3 as sql
from create_bot import bot
from telegram_bot_pagination import InlineKeyboardPaginator
from aiogram import types
from keyboards import inline
import math
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


genres = dict([(1,('%Аниме%',)),(2,('%Биография%',)),(3,('%Боевик%',)),(4,('%Вестерн%',)),(5,('%Военный%',)),(6,('%Детектив%',)),(7,('%Документальные%',)),(8,('%Драма%',)),\
    (9,('%Исторические%',)),(10,('%Комедия%',)),(11,('%Криминал%',)),(12,('%Мультфильмы%',)),(13,('%Приключения%',)),(14,('%Спортивные%',)),(15,('%Триллер%',)),(16,('%Ужасы%',)),\
        (17,('%Фантастика%',)),(18,('%Фэнтези%',))])

top = dict([(1,('Святые из Гетто(The Boondock Saints)',)),(2,('Тренер Картер(Coach Carter)',)),(3,('Властелин Колец(The Lord of the Rings)',)),(4,("Достучаться до небес(Knockin' on Heaven's Door)",)),(5,('Крестный отец(The Godfather)',)),\
    (6,('Лицо со шрамом(Scarface)',)),(7,('Троя(Troy)',)),(8,('Славные парни(Goodfellas)',)),(9,('Наруто(Naruto)',)),(10,('Движение Вверх',))])


class MyPaginator(InlineKeyboardPaginator):
    first_page_label = '⏪'
    previous_page_label = '{}'
    current_page_label = '·{}·'
    next_page_label = '{}'
    last_page_label = '⏩'

def sql_start():
    global base, cur
    base = sql.connect('films.db')
    cur = base.cursor()
    if base:
        print('Data base connected successfull')
    base.execute('CREATE TABLE IF NOT EXISTS film(id integer PRIMARY KEY AUTOINCREMENT ,img TEXT , name TEXT ,genre TEXT,description TEXT,date TEXT,rate integer)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO film(img,name,genre,description,date,rate) VALUES (?,?,?,?,?,?)',tuple(data.values()))
        base.commit()


async def sql_show_variant(chatid,code):
    for x in cur.execute('SELECT * FROM film WHERE id == ?',(code,)).fetchall():
        await bot.send_photo(chatid,x[1],f'_{x[2]}_\n*Жанр:* {x[3]}\n*Описание:* {x[4]}\n*Дата создания:* {x[5]}\n*Рейтинг:* {x[-1]}',parse_mode='Markdown')


async def sql_show_top(id,code = top.keys()):
    if(type(code) is int):
        for x in cur.execute('SELECT * FROM film WHERE name == ?',(top.get(code))).fetchall():
            await bot.send_photo(id,x[1],f'{x[2]}\n*Жанр:* {x[3]}\n*Описание:* {x[4]}\n*Дата создания:* {x[5]}\n*Рейтинг:* {x[-1]}',parse_mode='Markdown')
    else:
        inlinekeyboard = InlineKeyboardMarkup(row_width=1)
        for key in code:
            list = cur.execute('SELECT * FROM film WHERE name == ?',(top.get(key))).fetchall()
            for i in list:
                b = InlineKeyboardButton(text=f'{key}.{i[2]} {i[-1]}/10',callback_data=f'/f{i[0]}')
                inlinekeyboard.add(b)
    await bot.send_message(id,text='*TOP*🔟',reply_markup=inlinekeyboard,parse_mode='Markdown')

async def send_film_page(message : types.Message,film = 1):
        paginator = MyPaginator(page_count=cur.execute('SELECT COUNT(*) FROM film').fetchall()[0][0],current_page=film,data_pattern='film#{page}')
        for x in cur.execute('SELECT * FROM film WHERE id == ?',(film,)).fetchall():
            await bot.send_photo(message.chat.id,x[1],f'{x[2]}\n*Жанр:* {x[3]}\n*Описание:* {x[4]}\n*Дата создания:* {x[5]}\n*Рейтинг:* {x[-1]}',reply_markup=paginator.markup,parse_mode='Markdown')

async def send_inrate_order(message:types.CallbackQuery,rate,page = 1):
    # result = ''
    # lst =  cur.execute('SELECT * FROM film WHERE rate == ? ORDER BY rate DESC',((rate,))).fetchall()
    # for x in lst:
    #     result += f'{lst.index(x)+1}.{x[2]} {x[-1]}/10 /f{x[0]}\n'
    # await bot.send_message(message.from_user.id,text =f'Фильмы с оценкой *{rate}*:\n_{result}_',parse_mode='Markdown')
    inlinekeyboard = InlineKeyboardMarkup(row_width=1)
    list = cur.execute('SELECT * FROM film WHERE rate ==? ORDER BY rate DESC ',((rate,))).fetchall()
    if(len(list) > 10):
        count_pages = math.ceil(len(list)/10)
        paginator = InlineKeyboardPaginator(page_count = count_pages,current_page=page,data_pattern=f'forrate#{"{page}"}:{rate}')
        for i in list[(page-1)*10:len(list)-(len(list)-((page)*10))]:
            paginator.add_before(InlineKeyboardButton(text=f'{list.index(i)+1}.{i[2]} {i[-1]}/10',callback_data=f'/f{i[0]}'))
        await bot.send_message(chat_id=message.chat.id,text=f'Фильмы с оценкой *{rate}*:\n',reply_markup=paginator.markup,parse_mode='Markdown')
    else:
        for i in list:
            b = InlineKeyboardButton(text=f'{list.index(i)+1}.{i[2]} {i[-1]}/10',callback_data=f'/f{i[0]}')
            inlinekeyboard.add(b)
        await bot.send_message(chat_id=message.chat.id,text=f'*Фильмы с оценкой *{rate}*:\n*',reply_markup=inlinekeyboard,parse_mode='Markdown')


async def pages(message : types.Message,page = 1):
    count = math.ceil(cur.execute('SELECT COUNT(*) FROM film').fetchall()[0][0]/10) #количество страниц
    paginator = InlineKeyboardPaginator(page_count = count,current_page=page,data_pattern='page#{page}')
    y = math.ceil((cur.execute('SELECT COUNT(*) FROM film').fetchall()[0][0])/count) #количество фильмов на странице
    list = cur.execute('SELECT * FROM film WHERE id > ? LIMIT ?',((page * y) - y,y)).fetchall()
    for i in list:
        paginator.add_before(InlineKeyboardButton(text=f'{(list.index(i)+1)+((page-1)*y)}.{i[2]} {i[-1]}/10',callback_data=f'/f{i[0]}'))
    await bot.send_message(message.chat.id,text='Все фильмы на данный момент:',reply_markup=paginator.markup,parse_mode='Markdown')

def sql_read2():
    return cur.execute('SELECT * FROM film').fetchall()

def sql_delete_command(data):
    cur.execute('DELETE FROM film WHERE name == ?',(data,))
    base.commit()


async def sql_genre_filter(chatid : types.Message,code,page = 1):
    inlinekeyboard = InlineKeyboardMarkup(row_width=1)
    list = cur.execute('SELECT * FROM film WHERE genre LIKE ?',(genres.get(code))).fetchall()
    if(len(list) > 10):
        count_pages = math.ceil(len(list)/10)
        paginator = InlineKeyboardPaginator(page_count = count_pages,current_page=page,data_pattern=f'forgenre#{"{page}"}:{code}')
        for i in list[(page-1)*10:len(list)-(len(list)-((page)*10))]:
            paginator.add_before(InlineKeyboardButton(text=f'{list.index(i)+1}.{i[2]} {i[-1]}/10',callback_data=f'/f{i[0]}'))
        await bot.send_message(chat_id=chatid.chat.id,text=f'{genres.get(code)[0].replace("%","")}:\n',reply_markup=paginator.markup,parse_mode='Markdown')
    else:
        for i in list:
            b = InlineKeyboardButton(text=f'{list.index(i)+1}.{i[2]} {i[-1]}/10',callback_data=f'/f{i[0]}')
            inlinekeyboard.add(b)
        await bot.send_message(chat_id=chatid.chat.id,text=f'*{genres.get(code)[0].replace("%","")}:\n*',reply_markup=inlinekeyboard,parse_mode='Markdown')



    #for x in list:
        #await bot.send_message(chat_id=chatid,text=f'{x[2]} {x[-1]}/10')
        #result += f'_{list.index(x)+1}.{x[2]} {x[-1]}/10 /f{x[0]}\n_'
        #result += f'{x[2]} {x[-1]}/10 `/f{x[0]}`\n'
    #result = f'*{genres.get(code)[0].replace("%","")}:*\n{result}'
    #result


def sql_all():
    result = ''
    for x in cur.execute('SELECT * FROM film').fetchall():
        result += f'{x[2]} {x[-1]}/10 /f{x[0]}\n'
    return result



    