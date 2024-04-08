from RussianDeclensions import declension
from Constants import month_keys

import datetime
import requests


def get_time_now(**kwargs):
    """
    Функция для получения актуального времени, с точностью до минут.

    :return: Строка в формате 'Сейчас X часов Y минут.'
    """

    current_time = datetime.datetime.now()

    hours = current_time.hour
    minutes = current_time.minute

    return f"Сейчас { hours } { declension(hours, 'час') } { minutes } { declension(minutes, 'минута') }."


def get_date(**kwargs):
    """
    Функция для получения актуальной даты.

    :return: Строка, обозначающая дату, в формате "Сегодня ..."
    """

    current_date = datetime.date.today()

    day = current_date.day
    month = current_date.month
    year = current_date.year

    return f"Сегодня { day } { month_keys[month - 1] } { year } года."


def get_currency_course(**kwargs):
    """
    Функция для получения актуального курса валют, а именно доллара и евро.

    :return: Актуальный курс валют на данный момент в формате "Доллар - A рублей B копеек. Евро - C рублей D копеек."
             В случае непредвиденной ошибки возвращает строку с соответствующим предупреждением.
    """

    error_phrase = kwargs["__error_phrase"]
    try:
        data = requests.get(
            url="https://www.cbr-xml-daily.ru/daily_json.js",
            timeout=1
        ).json()

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
        return error_phrase


def get_weather_now(**kwargs):
    """
    Функция для получения текущей погоды. В качестве параметра принимает название города (опционально).
    В случае, если город не передан, будет использован город по умолчанию.

    :return: Актуальная погода запрошенном месте, в том числе температура, влажность, давление, ветер.
             В случае непредвиденной ошибки возвращает строку с соответствующим предупреждением.
    """

    open_weather_token = "e37d54207830a94eee9d3babc8b0d27f"

    city = kwargs["city"] if kwargs["info"] is None else kwargs["info"]

    is_celsium = kwargs["celsium"]
    is_mmHg = kwargs["mmHg"]
    error_phrase = kwargs["__error_phrase"]
    not_found_phrase = kwargs["__not_found_phrase"]

    try:
        r = requests.get(
            url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric",
            timeout=1
        )

        data = r.json()
        if data["cod"] == "404":
            return not_found_phrase

        cur_weather = int(data["main"]["temp"])
        feel = int(data['main']['feels_like'])
        humidity = int(data["main"]["humidity"])
        pressure = int(data["main"]["pressure"])
        wind = int(data["wind"]["speed"])

        def prepare_result():
            result = f"Погода в городе { city } \n"

            temp1 = cur_weather if is_celsium else int(cur_weather * 9 / 5) + 32
            temp1_pf = " " + declension(temp1, 'фаренгейт')
            result += (f"Температура: {'+' if temp1 > 0 else ''}{ temp1 }"
                       f"{'°' if is_celsium else temp1_pf} \n")

            temp2 = feel if is_celsium else int(feel * 9 / 5) + 32
            temp2_pf = " " + declension(temp2, 'фаренгейт')
            result += (f"Ощущается как {'+' if temp2 > 0 else ''}{ temp2 }"
                       f"{'°' if is_celsium else temp2_pf} \n")

            result += f"Влажность: { humidity }% \n"

            prs = int(pressure * 3 / 4) if is_mmHg else pressure
            prs_phrase = f"милли{ declension(prs, 'метр') } ртутного столба" if is_mmHg \
                else f"гекто{ declension(prs, 'паскаль')}"

            result += f"Давление: { prs } { prs_phrase } \n"
            result += f"Ветер: { wind } { declension(wind, 'метр') } в секунду. \n"

            return result

        return prepare_result()
    except Exception:
        return error_phrase
