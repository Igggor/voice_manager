import datetime, requests
import speech_recognition


from gtts import gTTS
import os

# ЭТОТ ФАЙЛ БУДЕТ УДАЛЕН, А ВСЕ ФУНКЦИИ ПЕРЕНЕСЕНЫ.
pass

# sr = speech_recognition.Recognizer()
# sr.pause_threshold = 0.5
# r = speech_recognition.Recognizer()
# m = speech_recognition.Microphone(device_index=1)
#
# def create_task():#Создание заметки в todo листе
#     speak('Что добавим в список дел?')
#     query = listen_command()
#     with open('../todo-list.txt', 'a') as file:
#         file.write(f'{query}\n')
#     return f'Задача {query} создана и добавлена в список задач'
#
# def curs():
#     data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
#     usd = round(data['Valute']['USD']['Value'], 2)
#     euro = round(data['Valute']['EUR']['Value'], 2)
#     usd_rub = int(usd)
#     usd_kop = int(round(usd - int(usd), 2) * 100)
#     euro_rub = int(euro)
#     euro_kop = int(round(euro - int(euro), 2) * 100)
#     return  (f"Курс валют сейчас:\n"
#           f"Доллар можно купить за {usd_rub} {sclon(usd_rub, 'rub')} {usd_kop} {sclon(usd_kop, 'kop')}.\n"
#           f"Евро можно купить за {euro_rub} {sclon(euro_rub, 'rub')} {euro_kop} {sclon(euro_kop, 'kop')}.\n"
#           )
#
#
# def weather():
#     speak("В каком городе ты хочешь узнать погоду?")
#     city = listen_command()
#     print(f"[Log] распознан город {city}")
#     return get_weather(city)
#
#
# def get_weather(city, open_weather_token = "e37d54207830a94eee9d3babc8b0d27f"):
#     try:
#         r = requests.get(
#             f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
#         )
#         data = r.json()
#
#         city = data["name"]
#         cur_weather = data["main"]["temp"]
#
#         humidity = data["main"]["humidity"]
#         pressure = data["main"]["pressure"]
#         wind = data["wind"]["speed"]
#         feel = data['main']['feels_like']
#         return (f"Погода в городе: {city}\nТемпература: {cur_weather}° \nОщущается как {feel}°\n"
#               f"Влажность: {humidity}%\nДавление: {pressure} Паскалей \nВетер: {wind} метров в секунду\n")
#
#     except Exception as ex:
#         print(ex)
#         return "Проверьте название города"
#
#
# def sclon(a, txt):
#     if(txt == "rub"):
#         if (a // 10 != 1) and (a % 10 == 1):
#             return ("Рубль")
#         elif (a // 10 != 1) and (a % 10 == 2 or a % 10 == 3 or a % 10 == 4):
#             return ("Рубля")
#         elif (a // 10 != 1) and (a % 10 == 5 or a % 10 == 6 or a % 10 == 7 or a % 10 == 8 or a % 10 == 9 or a % 10 == 0):
#             return (("Рублей"))
#         else:
#             return (("Рублей"))
#     if (txt == "kop"):
#         if (a // 10 != 1) and (a % 10 == 1):
#             return ("Копейку")
#         elif (a // 10 != 1) and (a % 10 == 2 or a % 10 == 3 or a % 10 == 4):
#             return ("Копейки")
#         elif (a // 10 != 1) and (a % 10 == 5 or a % 10 == 6 or a % 10 == 7 or a % 10 == 8 or a % 10 == 9 or a % 10 == 0):
#             return (("Копеек"))
#         else:
#             return (("Копеек"))