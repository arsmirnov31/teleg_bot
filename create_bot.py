import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher ## Отлавливает события

from aiogram.contrib.fsm_storage.memory import MemoryStorage ## Хранилище для FSM 

storage=MemoryStorage()
#
bot = Bot(token=os.getenv('TOKEN')) ## Создаем объект бота, token берется из переменных сред 
dp = Dispatcher(bot, storage=storage) ## Добавляем боту обработчик событий и место хранения ответов от пользователей (Оперативная память) 