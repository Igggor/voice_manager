import datetime

from RussianDeclensions import *


def getTimeNow():
    currentTime = datetime.datetime.now()

    hours = currentTime.hour
    minutes = currentTime.minute

    return f"Сейчас { hours } { declension(hours, 'час') } { minutes } { declension(minutes, 'минута') }."
