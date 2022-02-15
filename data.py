import requests
import time
import pandas
import json

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.46'}
url = 'https://api.hh.ru/vacancies/'
text = input("Название вакансии: ")
area = int(input("Область поиска, 1 - Москва, 1438 - Краснодарский край: "))

def get_data(page = 0):    # Функция на проведение GET запроса к API HH.ru, для получения данных
    params = {
        'text': text,    # Наименование вакансии
        'area': area,    # Область/город поиска
        'page': page,    # Количество страниц с данными
        'per_page': 100,    # Количество вакансия на одну страницу
        'only_with_salary': 'True'    # Поиск вакансия в которых указана зарплата
    }

    req = requests.get(url, params, headers=headers)
    data = req.content.decode()
    req.close()
    return data

start_time = time.time()    # Начало выполнения скрипта

itog_json = []
for page in range(0, 20):    # Цикл получения данных со страниц
    info = json.loads(get_data(page))    # Запуск функции, перевод данных в JSON формат
    itog_json.extend(info["items"])    # Добавление данных в список
    if (info["pages"] - page) <= 1:    # Проверка, на случай если менее 20 страниц - остановка цикла
        break
    time.sleep(0.25)    # Временная задержка, для снижения нагрузки на сервер

print("--- %s seconds ---" % (time.time() - start_time))    # Окончание времени получения данных

dt = []    # Список для фильтрации данных
for item in itog_json:
    new_row = {
        "Наименование": item["name"],
        "Город": item["area"]["name"],
        "Зарплата от": item["salary"]["from"],
        "Зарплата до": item["salary"]["to"],
        "Валюта": item["salary"]["currency"],
        "Требования": item['snippet']['requirement'],
        "Обязанности": item['snippet']['responsibility'],
        "Условие": item['schedule']['name'],
        "Ссылка": item['alternate_url']
    }
    dt.append(new_row)
DATA = pandas.DataFrame(dt)    # Перевод отфильтрованных данных в DataFrame
writer = pandas.ExcelWriter('my_data.xlsx')    # Создание excel-файла
DATA.to_excel(writer)    # Запись данных в excel
writer.save()    # Сохранение данных
print('DataFrame записан в Excel')