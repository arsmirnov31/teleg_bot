from os import curdir
import sqlite3 as sq
from create_bot import bot
from file_utilities import blob_file
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def sql_start():
    global base, cur
    base = sq.connect('tel_bot_mem.db')
    cur = base.cursor()
    if base:
        print('Database Connected OK!')
    
## Запрос для добавления строки в БД
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO main_memory (mem_image, date, mem_message) VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

# Запрос на вывод данных по дате события
async def sql_read(message, date_filter):
    print('Пытаюсь выполнить запрос')
    for ret in cur.execute('Select date, mem_message, mem_image, mem_id from main_memory Where date = ?', (date_filter, )).fetchall():
        file = blob_file.writeTofile(ret[2])
        await bot.send_photo(message.from_user.id, open(file, 'rb'), f'Описание: {ret[1]}\nId письма: {ret[3]}', reply_markup= InlineKeyboardMarkup().\
            add(InlineKeyboardButton(f'Удалить {ret[3]}', callback_data=f'del {ret[3]}')))

# Запрос для вывода рандомного события
async def sql_rand(message):
    print('Пытаюсь выполнить запрос')
    for ret in cur.execute('Select date, mem_message, mem_image, mem_id from main_memory ORDER BY RANDOM() LIMIT 1').fetchall():
        file = blob_file.writeTofile(ret[2])
        await bot.send_photo(message.from_user.id, open(file, 'rb'), f'Описание: {ret[1]}\nДата события: {ret[0]}\nId письма: {ret[3]}', reply_markup= InlineKeyboardMarkup().\
            add(InlineKeyboardButton(f'Удалить {ret[3]}', callback_data=f'del {ret[3]}')))


# async def sql_get_all(id):
#     cur.execute('Select * from main_memory').fetchall()
#     base.commit()


## Запрос для удаления строки
async def sql_del(id):
    cur.execute('Delete from main_memory Where mem_id == ?', (id,))
    base.commit()

        