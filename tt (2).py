# from aiogram.utils.callback_data import CallbackData
film_cb = CallbackData('film_callback', 'action', 'cur_page')
page_cb = CallbackData('page_callback', 'next_page')

# ...

def get_film_kb(page_number: int) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Назад', callback_data=film_cb.new('back', page_number))
    inline_keyboard.row(b1)
    return inline_keyboard

def get_page_kb(page_number: int) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    # sql запрос туда сюда, получаешь фильмы по page_number и не выёбываешься
    for i in range(1 + (page_number - 1) * 10, 1 + (page_number)*10):
        b = InlineKeyboardButton(text=f'Фильм {i}', callback_data=film_cb.new('open_film', page_number))
        inline_keyboard.add(b)
    b1 = InlineKeyboardButton(text='<', callback_data=page_cb.new(page_number - 1))
    b2 = InlineKeyboardButton(text='>', callback_data=page_cb.new(page_number + 1))
    inline_keyboard.row(b1, b2)
    return inline_keyboard

async def command_list(user_message: types.Message):
    list_message = await user_message.answer('Загрузка')
    cur_page = 1

    inline_keyboard = get_page_kb(cur_page)

    await list_message.edit_text('Все фильмы: (условно)', reply_markup=inline_keyboard)
    
@dp.callback_query_handler(film_cb.filter())
async def process_callback_film(query: types.CallbackQuery, callback_data: dict):
    list_message = query.message
    action = callback_data['action']
    cur_page = int(callback_data['cur_page'])
    try:
        match action:
            case 'open_film':
                inline_keyboard = get_film_kb(cur_page)
                await list_message.edit_text('Карточка фильма', reply_markup=inline_keyboard)
            case 'back':
                inline_keyboard = get_page_kb(cur_page)
                await list_message.edit_text('Все фильмы (условно)', reply_markup=inline_keyboard)
            case _:
                print('Ошибка, нет такого действия')
    except:
        print('Ошибка в process_callback_film')
    # кнопка фильма
    # вывод фильма
    # благодаря list_message можно вывести в текущем сообщении

@dp.callback_query_handler(page_cb.filter())
async def process_callback_page(query: types.CallbackQuery, callback_data: dict):
    list_message = query.message
    next_page = int(callback_data['next_page'])
    inline_keyboard = get_page_kb(next_page)
    try:
        await list_message.edit_text('Все фильмы: (условно)', reply_markup=inline_keyboard)
    except:
        print('Ошибка в process_callback_page')