from RussianDeclensions import declension
from Constants import month_keys
from Classes import Response

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

    return Response(
        text=f"Сейчас { hours } { declension(hours, 'час') } { minutes } { declension(minutes, 'минута') }."
    )


def get_date(**kwargs):
    """
    Функция для получения актуальной даты.

    :return: Строка, обозначающая дату, в формате "Сегодня ..."
    """

    current_date = datetime.date.today()

    day = current_date.day
    month = current_date.month
    year = current_date.year

    return Response(
        text=f"Сегодня { day } { month_keys[month - 1] } { year } года."
    )


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

        output_text = (f"Курс валют на данный момент:\n"
                       f"Доллар - { usd[0] } { declension(usd[0], 'рубль') } "
                       f"{ usd[1] } { declension(usd[1], 'копейка') }.\n"
                       f"Евро - { euro[0] } { declension(euro[0], 'рубль') } "
                       f"{ euro[1] } { declension(euro[1], 'копейка') }."
                       )

        return Response(
            text=output_text
        )
    except:
        return Response(
            text=error_phrase,
            is_correct=False
        )


def get_weather_now(**kwargs):
    """
    Функция для получения текущей погоды. В качестве параметра принимает название города (опционально).
    В случае, если город не передан, будет использован город по умолчанию.

    Опциональные параметры:
        * ``city``: город, для которого необходимо определить погоду. Если не задан, будет определена
        погода для города по умолчанию.

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
            return Response(
                header=not_found_phrase,
                text=city,
                is_correct=False,
                type="city-not-found-error"
            )

        cur_weather = int(data["main"]["temp"])
        feel = int(data['main']['feels_like'])
        humidity = int(data["main"]["humidity"])
        pressure = int(data["main"]["pressure"])
        wind = int(data["wind"]["speed"])
        weather_key = str(data["weather"][0]["id"])

        def get_translation():
            if weather_key[0] == '2':
                return "Гроза. \n"
            if weather_key[0] == '3':
                return "Слабый дождь. \n"
            if weather_key[0] == '5':
                return "Дождь. \n"
            if weather_key[0] == '6':
                return "Снег. \n"
            if weather_key[0] == '8':
                return "Облачно. \n"

            return "Ясно. \n" if weather_key == "800" else None

        def prepare_result():
            result = f"Погода в городе { city }. \n"
            weather_state = get_translation()
            if weather_state is not None:
                result += weather_state

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
            result += f"Ветер: { wind } { declension(wind, 'метр') } в секунду."

            return result

        return Response(
            text=prepare_result()
        )
    except Exception:
        return Response(
            text=error_phrase,
            is_correct=False
        )
