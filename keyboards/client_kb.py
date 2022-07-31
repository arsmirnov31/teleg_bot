#from requests import request
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton##, ReplyKeyboardRemove

b1 = KeyboardButton('/random_date')
b2 = KeyboardButton('Я заблудился', request_location=True)
b3 = KeyboardButton('/Вводим_дату')
b4 = KeyboardButton('/модератор')
b5 = KeyboardButton('/отмена')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).insert(b2).add(b3).insert(b4).add(b5)


## , one_time_keyboard= True