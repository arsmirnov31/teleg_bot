import urllib.request
import json
import os

## функция по конвертации файла в бинарный вид 
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def writeTofile(data):
    # Convert binary data to proper format and write it on Hard Disk
    with open('filename', 'wb') as file:
        file.write(data)
    return 'filename'

def get_blob_file (token, file_id):
    # Формируем ссылку с справочной информацией 
    link =  'https://api.telegram.org/bot{}/getFile?file_id={}'.format(token, file_id)
    # Открываем ссылку 
    webUrl  = urllib.request.urlopen(link)

    # Читаем полученные данные 
    data = webUrl.read()
    # Конвертируем в Json
    stud_obj = json.loads(data)
    # Находим файл 
    download_link = 'https://api.telegram.org/file/bot{}/{}'.format(token, stud_obj['result']['file_path'])
    file = urllib.request.urlopen(download_link)

    #Скачиваем файл скорее всего он уже в бинарном виде
    urllib.request.urlretrieve(download_link, '.\image1')
    #blob_data = convertToBinaryData('.\image1')
    
    #return(blob_data)
    return(file.read())
