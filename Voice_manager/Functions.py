import datetime

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
