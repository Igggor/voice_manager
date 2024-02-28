import datetime
import requests

from RussianDeclensions import *


monthKeys = ["января", "февраля", "марта", "апреля", "мая", "июня",
             "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def getTimeNow():
    currentTime = datetime.datetime.now()

    hours = currentTime.hour
    minutes = currentTime.minute

    return f"Сейчас { hours } { declension(hours, 'час') } { minutes } { declension(minutes, 'минута') }."


def getDate():
    currentDate = datetime.date.today()

    day = currentDate.day
    month = currentDate.month
    year = currentDate.year

    return f"Сегодня { day } { monthKeys[month - 1] } { year } года."


def getCurrencyCourse():
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

        usdFormal = round(data['Valute']['USD']['Value'], 2)
        euroFormal = round(data['Valute']['EUR']['Value'], 2)

        usd = [int(usdFormal * 100) // 100, int(usdFormal * 100) % 100]
        euro = [int(euroFormal * 100) // 100, int(euroFormal * 100) % 100]

        return (f"Курс валют на данный момент:\n"
                f"Доллар - { usd[0] } { declension(usd[0], 'рубль') } "
                f"{ usd[1] } { declension(usd[1], 'копейка') }.\n"
                f"Евро - { euro[0] } { declension(euro[0], 'рубль') } "
                f"{ euro[1] } { declension(euro[1], 'копейка') }.\n"
                )
    except:
        return "Извините, во время получения данных произошла непредвиденная ошибка. Повторите запрос позднее."
