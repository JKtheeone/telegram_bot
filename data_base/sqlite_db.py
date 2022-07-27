import sqlite3 as sql
from create_bot import bot

def sql_start():
    global base, cur
    base = sql.connect('films.db')
    cur = base.cursor()
    if base:
        print('Data base connected successfull')
    base.execute('CREATE TABLE IF NOT EXISTS film(id integer primary key autoincrement, img TEXT, name TEXT, genre TEXT, description TEXT, date TEXT, rate TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO film(img, name, genre, description, date, rate) VALUES (?,?,?,?,?,?)',tuple(data.values()))
        base.commit()

async def sql_show_variant(id, film_id):
    for x in cur.execute('SELECT * FROM film WHERE id == ?',(film_id,)).fetchall():
        await bot.send_photo(id,x[1],f'{x[2]}\nЖанр: {x[3]}\nОписание: {x[4]}\nДата создания: {x[5]}\nРейтинг: {x[-1]}')

#async def sql_show_variant(callback_query):
    #for x in cur.execute('SELECT * FROM film WHERE name == ?',('first movie',)).fetchall():
        #await bot.send_photo(callback_query.from_user.id,x[0])
        #await bot.answer_callback_query(callback_query.from_user.id,f'{x[1]}\nЖанр: {x[2]}\nОписание: {x[3]}\nДата создания: {x[4]}\nРейтинг: {x[-1]}')

async def sql_get():
    films = cur.execute('SELECT id, name FROM film').fetchall()
    message, indices = zip(*films)
    message = '\n'.join(f"{i + 1}. {value}" for i, value in enumerate(message))
    return { 'message': message, 'indices': indices }

async def sql_read(message):
    films = cur.execute('SELECT name FROM film').fetchall()
    y = '\n'.join(f"{i + 1}. {value[0]}" for i, value in enumerate(films))
    #y = '\n'.join("{0}".format(*value) for value in x)
    #y = '\n'.join(str(value).replace(",()'",'').replace("'","").replace('(','').replace(')','') for value in x)
    await bot.send_message(message.from_user.id, y) #f'{ret[1]}\nЖанр: {ret[2]}\nОписание: {ret[3]}\nДата создания: {ret[4]}\nРейтинг: {ret[-1]}')