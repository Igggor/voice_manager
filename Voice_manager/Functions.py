import datetime
import requests

from RussianDeclensions import *


monthKeys = ["января", "февраля", "марта", "апреля", "мая", "июня",
             "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def get_time_now():
    """
    Функция для получения актуального времени, с точностью до минут.

    :return: Строка в формате 'Сейчас X часов Y минут.'
    """
    current_time = datetime.datetime.now()

    hours = current_time.hour
    minutes = current_time.minute

    return f"Сейчас { hours } { declension(hours, 'час') } { minutes } { declension(minutes, 'минута') }."


def get_date():
    """
    Функция для получения актуальной даты.

    :return: Строка, обозначающая дату, в формате "Сегодня ..."
    """
    current_date = datetime.date.today()

    day = current_date.day
    month = current_date.month
    year = current_date.year

    return f"Сегодня { day } { monthKeys[month - 1] } { year } года."


def get_currency_course():
    """
    Функция для получения актуального курса валют, а именно доллара и евро.

    :return: Актуальный курс валют на данный момент в формате "Доллар - A рублей B копеек. Евро - C рублей D копеек."
             В случае непредвиденной ошибки возвращает строку с соответствующим предупреждением.
    """
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

        usd_formal = round(data['Valute']['USD']['Value'], 2)
        euro_formal = round(data['Valute']['EUR']['Value'], 2)

        usd = [int(usd_formal * 100) // 100, int(usd_formal * 100) % 100]
        euro = [int(euro_formal * 100) // 100, int(euro_formal * 100) % 100]

        return (f"Курс валют на данный момент:\n"
                f"Доллар - { usd[0] } { declension(usd[0], 'рубль') } "
                f"{ usd[1] } { declension(usd[1], 'копейка') }.\n"
                f"Евро - { euro[0] } { declension(euro[0], 'рубль') } "
                f"{ euro[1] } { declension(euro[1], 'копейка') }.\n"
                )
    except:
        return "Извините, во время получения данных произошла непредвиденная ошибка. Повторите запрос позднее."
