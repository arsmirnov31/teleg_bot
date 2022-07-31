@echo off

call %~dp0\telegram_bot\venv\Scripts\activate

cd %~dp0\telegram_bot

set TOKEN=5343247323:AAFZ5GJxS7OLq6FwdahZNEHb5LIXiWLq314

python main_bot.py

pause