from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data_base import sqlite_db
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ID = []

def check_date (string):
    try:
        date = datetime.datetime.strptime(string,"%d.%m.%Y")
        print(date)
        return date
    except:
        print('Не получилось')
        date =None
        return date


class FSMUser(StatesGroup):
    input_date = State()
    check_date = State()
    send_message = State()


## Вводное сообщение с описанием
#@dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    if message.from_user.id in ID:
        try: 
            #await message.reply('Приветственное сообщение', reply_markup = kb_client)
            await bot.send_message(message.from_user.id, 'На клавиатуре нужно выбрать кнопка "Ввода данных"', reply_markup = kb_client)
            await message.delete()
        except:
            await message.reply('Общение с ботом возможно по инициативе пользователя, напишите ему \n https://t.me/zhenya_call_bot ')

## Запускам конечный автомат и просим ввести дату
#@dp.message_handler(commands='Вводим_дату')
async def fms_start(message : types.Message):
    if message.from_user.id in ID: ## Проверка пользователя, что оно администратор группы, его нужно писать во все хендлеры, где нужно повышение прав доступа.
        print('Начинаем ввод данных')
        await FSMUser.input_date.set()
        await message.reply('Введите дату в формате 22.02.2022')


## Проверяем корректность ввода даты
#@dp.message_handler(lambda message: not check_date(message.text), state=FSMUser.input_date)
async def process_date_invalid(message: types.Message):
    '''
    Дата введена не корректно
    '''
    return await message.reply("Дата должна быть в формате 22.02.2022 (День, месяц, год) через точку")


## Записываем дату 
#@dp.message_handler(lambda message: not check_date(message.text), state=FSMUser.input_date)
async def input_data(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        print('Я пытаюсь получить дату')
        async with state.proxy() as data:
            data['date'] = message.text
        await sqlite_db.sql_read(message, data['date'])
        #await message.reply('Сейчас увидим события за дату')
        #await FSMUser.next()
        await state.finish()


## Отменить ввод данных
async def cancel_handler_user(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        print('Я пытаюсь остановится')
        current_state = await state.get_state()
        if current_state is None:
            print('Я пытаюсь остановится')
            return
        await state.finish()
        await message.reply('Отмена операции')



#@dp.message_handler(commands=['random_date'])
async def get_random_event(message : types.Message):
    if message.from_user.id in ID:
        await sqlite_db.sql_rand(message)


def register_handlers_client (dp : Dispatcher):
    dp.register_message_handler(cancel_handler_user, state = "*", commands = ['отмена'])
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(get_random_event, commands=['random_date'])
    dp.register_message_handler(fms_start, commands=['Вводим_дату'], state=None)
    dp.register_message_handler(process_date_invalid, lambda message: not check_date(message.text), state=FSMUser.input_date)
    dp.register_message_handler(input_data, lambda message: check_date(message.text), state=FSMUser.input_date)
    
