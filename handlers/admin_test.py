from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from aiogram.types import ParseMode

ID = None

4# States

class FSMAdmin(StatesGroup):
    add_photo = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'

# Получаем ID текущего модератора, Id будет записан только в том случае, если пользователь является администратором группы
#@dp.message_handler(commands=['модератор'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо')#, reply_markup=button_case_admin)
    await message.delete()


#@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Создаем входную точку
    """
    # Set state
    print('Начинаем Диалог')
    await FSMAdmin.add_photo.set()
    await message.reply("прикрепите фотографию")



#@dp.message_handler(state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    """
    Процесс добавления фото
    """
    print('Я пытаюсь инициировать загрузку фото')

    async with state.proxy() as data:
        data['photo'] = 'photo' ### МЫ НЕ ПИШЕМ САМ ФАЙЛ В БД ЦЕЛИКОМ А ТОЛЬКО ЕГО ID
        print('Я добрался до загрузки фотографии')

    await FSMAdmin.next()
    await message.reply("How old are you?")





#@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await FSMAdmin.next()
    await state.update_data(age=int(message.text))
    await message.reply("What is your gender?")


#@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Hi! Nice to meet you,', md.bold(data['photo'])),
                md.text('Age:', md.code(data['age'])),
                md.text('Gender:', data['gender']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()



def register_handlers_admin (dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.add_photo)
    dp.register_message_handler(process_age,  state=FSMAdmin.age)
    dp.register_message_handler(process_gender, state=FSMAdmin.gender)
