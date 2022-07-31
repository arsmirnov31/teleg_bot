# Import Required Library
from tkinter import *
from tkcalendar import Calendar ## Потребуется установить в вручную
from PIL import ImageTk, ImageTk
from tkinter import filedialog, messagebox
import sqlite3
import copy
import datetime

#Connection database

current_date =""
chosen_file_name =""

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def mem_date(date_):
    global current_date
    current_date = copy.copy(date_)
    choose_date = Label(root, text=date_, width=40, pady=50).grid(row=0, column= 1, sticky = W)
    cal_window.destroy()
    print(current_date)


def open_calc():
    '''Открываем окно с календарем'''
    global cal_window
    cal_window = Toplevel()
    cal = Calendar(cal_window, selectmode = 'day',
                year = 2022, month = 5,
                day = 22)
    memory_date_btn = Button(cal_window, text = "Запомнить", command=lambda: mem_date(cal.get_date()))
    cal.pack()
    memory_date_btn.pack()


def open_file():
    ## Очищаем Label от прошлого запроса 
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) == 1 and int(label.grid_info()["column"]) == 1:
            label.grid_forget()
    
    ## Выбираем файл
    root.filename = filedialog.askopenfilename(initialdir = "C:\Scripts", title="Выбери файл воспоминаний", filetypes=(("png files", "*.png"),("all files", "*.*")))
    ## Добавляем Label
    chosed_file = Label(root, text=root.filename, padx=20)
    chosed_file.grid(row=1, column =1, sticky = W)
    global chosen_file_name 
    chosen_file_name = root.filename


def save_in_db():
    # Получаем введенные сообщения 
    input_text =  message_entry.get("1.0","end")

    ## Различные проверки 
    if not current_date:
        messagebox.showwarning(title='Ошибка', message='Нужно выбрать дату')
        return
    elif not chosen_file_name and len(input_text) == 1:
        messagebox.showwarning(title='Ошибка', message='Выберете документ или сделайте пометку')
        return
    elif len(input_text) > 1 and not chosen_file_name:
         query = """ INSERT INTO main_memory
                    (mem_message, date) VALUES (?, ?)"""
         data_for_insert = (input_text, datetime.datetime.strptime(current_date, "%m/%d/%y").strftime("%Y-%m-%d"))
    elif chosen_file_name and len(input_text) == 1:
        blob_doc = convertToBinaryData(chosen_file_name)
        query = """ INSERT INTO main_memory
                    (mem_image, date) VALUES (?, ?)"""      
        data_for_insert = (blob_doc, datetime.datetime.strptime(current_date, "%m/%d/%y").strftime("%Y-%m-%d"))
    elif chosen_file_name and len(input_text) > 1:
        blob_doc = convertToBinaryData(chosen_file_name)
        query = """ INSERT INTO main_memory
                    (mem_message, mem_image, date) VALUES (?, ?, ?)"""      
        data_for_insert = (input_text, blob_doc, datetime.datetime.strptime(current_date, "%m/%d/%y").strftime("%Y-%m-%d"))

    # Пишем в БД информацию 
    conn = sqlite3.connect('tel_bot_mem.db')
    cur = conn.cursor()
    cur.execute(query, data_for_insert)
    conn.commit()
    conn.close()


def open_change_window():
    pass


def clear_window():
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) == 0 and int(label.grid_info()["column"]) == 1:
            label.grid_forget()
        elif int(label.grid_info()["row"]) == 1 and int(label.grid_info()["column"]) == 1:
            label.grid_forget()

    current_date =""
    chosen_file_name =""
    message_entry.delete("1.0","end")


# Создаем основной объект
root = Tk()

message_string = StringVar() ## Переменная для сохранения текста из сообщения
 
# Создаем надпись выбора даты
#
# Создаем кнопку, которая откроет календарь
open_cal_btn = Button(root, text="Выбери дату", command=open_calc).grid(row=0, column= 0, sticky = W)
# Создаем кнопку для получения документа
find_file_btn = Button(root, text="Выбери файл", command=open_file).grid(row=1, column=0, sticky = W)
# Создаем заголовок для текстового поля пометок
message_title = Label(root, text="Пометочки", pady= 100).grid(row=3, column= 0, sticky = W)
# Создаем поле для ввода пометок
message_entry = Text(root, width=50, height=10)
message_entry.grid(row=3, column = 1, sticky = W)
# Создаем кнопку для сохранения в БД
save_db_btn = Button(root, text="Сохранить", command=save_in_db).grid(row=4, column= 0, sticky = W)
# Кнопка редактирования
change_record_btn = Button(root, text="Редактировать записи", command=open_change_window).grid(row=4, column= 1, sticky = W)
# Кнопка для очистки ввода
clear_btn = Button(root, text="Очистить ввод", command=clear_window).grid(row=4, column= 2, sticky = W)












# # Создаем элемент - календарь
# cal = Calendar(root, selectmode = 'day',
#                year = 2022, month = 5,
#                day = 22).grid(row=0, column= 1)


# Добавляем кнопку 
# Button(root, text = "Добавить событие",
#        command = grad_date).grid(row=1, column= 1)

# Добавляем элементы


 

 


root.title("Мемасики бесконечны")
root.geometry("700x500+500+200")
#root.minsize(300, 400)
#root.maxsize(500, 600)
#root.resizable(True, True)
root.mainloop()