from aiogram.types import ReplyKeyboardMarkup, KeyboardButton##, ReplyKeyboardRemove
# Кнопки клавиатуры админа
button_load = KeyboardButton('/Загрузить')
button_start = KeyboardButton('/start')
button_cancel = KeyboardButton('/отмена')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
        .insert(button_start).add(button_cancel)