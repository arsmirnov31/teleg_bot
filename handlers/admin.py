from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from file_utilities import blob_file
import os
from data_base import sqlite_db
from keyboards import admin_kb
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


token=os.getenv('TOKEN')

def check_date (string):
    try:
        date = datetime.datetime.strptime(string,"%d.%m.%Y")
        return date
    except:
        date =None
        return date


ID = []



## Задаем состояния для конечного автомата
class FSMAdmin(StatesGroup):
    photo = State()
    event_date = State()
    description = State()

# Получаем ID текущего модератора, Id будет записан только в том случае, если пользователь является администратором группы
#@dp.message_handler(commands=['модератор'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    if message.from_user.id in ID:
        await message.reply('Грузим фотки', reply_markup=admin_kb.button_case_admin)
        #await bot.send_message(message.from_user.id, 'Что хозяин надо', reply_markup=admin_kb.button_case_admin)
        await message.delete()


## Начало диалога записи нового события
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
    if message.from_user.id in ID: ## Проверка пользователя, что оно администратор группы, его нужно писать во все хендлеры, где нужно повышение прав доступа.
        print('Начинаем Диалог')
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')


## Ловим первый ответ и пишем в словарь
#@dp.message_handler(commands=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        print('Я пытаюсь инициировать загрузку фото')
        async with state.proxy() as data:
            data['photo'] = blob_file.get_blob_file(token, message.photo[-1].file_id) ## -1 Для выбора фотографии с наибольшим разрешенением
            #data['photo'] = message.photo[-1].file_id ### МЫ НЕ ПИШЕМ САМ ФАЙЛ В БД ЦЕЛИКОМ А ТОЛЬКО ЕГО ID
            print('Я добрался до загрузки фотографии')
        await FSMAdmin.next()
        await message.reply('Напишите дату событи в формате 22.02.2022 (День, месяц, год) через точку')


async def process_date_invalid(message: types.Message):
    '''
    Дата введена не корректно
    '''
    print('Я прохожу проверку даты')
    return await message.reply("Дата должна быть в формате 22.02.2022 (День, месяц, год) через точку")

# ## Ловим второй ответ
# #@dp.message_handler(state=FSMAdmin.event_date)
async def load_date(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['event_date'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите описание")




## Ловим третий ответ
#@dp.message_hanlder(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['description'] = message.text
        
        await sqlite_db.sql_add_command(state)
            
        await state.finish() ## После этого словарь Дата удалится


#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case = True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Отмена FMS')

## Кнопка Обработчик кнопки удаления 
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_call_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_del(int(callback_query.data.replace('del ', '')))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удален.)', show_alert=True)


def register_handlers_admin (dp : Dispatcher):
    dp.register_message_handler(cancel_handler, state = "*", commands = ['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case = True), state = "*")
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state = FSMAdmin.photo)
    dp.register_message_handler(process_date_invalid, lambda message: not check_date(message.text), state = FSMAdmin.event_date)
    dp.register_message_handler(load_date, lambda message: check_date(message.text), state = FSMAdmin.event_date)
    dp.register_message_handler(load_description, state = FSMAdmin.description)
    ## Для события отмены мы описываем два хендлера, так как декоратора тоже было 2
    dp.register_message_handler(make_changes_command, commands=['модератор'])
    dp.register_message_handler(del_call_run, lambda x: x.data and x.data.startswith('del '))