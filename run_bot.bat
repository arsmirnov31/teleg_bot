@echo off

call %~dp0\telegram_bot\venv\Scripts\activate

cd %~dp0\telegram_bot

set TOKEN=

python main_bot.py

pause
