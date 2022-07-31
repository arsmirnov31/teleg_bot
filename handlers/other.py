from aiogram import types, Dispatcher
import json, string
from create_bot import dp

#@dp.message_handler()       ## Декоратор улавливает все сообщения написанные боту
async def echo_send(message : types.message):
    if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(" ")}\
        .intersection(set(json.load(open('censor.json')))) != set():
        await message.reply('Аларм Слово на букву К....')
        await message.delete()


def register_handlers_other (dp : Dispatcher):
    dp.register_message_handler(echo_send)

