from aiogram.utils import executor ## Запускает в двух режимах LongPolling(Постоянный опрос сервера телеграмма) и WebHook(деплой на какой либо сервер)
from create_bot import dp
from handlers import admin, client, other
from data_base import sqlite_db

async def on_startup(_):
    print('Я вышел онлайн')
    sqlite_db.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

