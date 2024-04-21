from Russian import declension
from Constants import MONTH_KEYS
from Classes import Response
from GlobalContext import GlobalContext

import datetime
import requests


class FunctionsCore:
    """
    Класс, содержащий в себе весь (за несколькими исключениями) функционал помощника.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(FunctionsCore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.weather_error_phrase = None
        self.weather_not_found_phrase = None
        self.weather_celsium = None
        self.weather_mmHg = None

        self.course_error_phrase = None
        self.city = None

    def update_settings(self):
        global_context = GlobalContext()

        self.weather_error_phrase = global_context.WEATHER_REQUEST_ERROR_PHRASE
        self.weather_not_found_phrase = global_context.WEATHER_NOT_FOUND_PHRASE
        self.weather_celsium = global_context.weather_temp_celsium
        self.weather_mmHg = global_context.weather_pressure_mmHg

        self.course_error_phrase = global_context.COURSE_REQUEST_ERROR_PHRASE
        self.city = global_context.CITY

    @staticmethod
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
            text=f"Сегодня { day } { MONTH_KEYS[month - 1] } { year } года."
        )

    def get_currency_course(self, **kwargs):
        """
        Функция для получения актуального курса валют, а именно доллара и евро.

        :return: Актуальный курс валют на данный момент в формате
                 ``"Доллар - A рублей B копеек. Евро - C рублей D копеек."``
                 В случае непредвиденной ошибки возвращает строку с соответствующим предупреждением.
        """

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
        except requests.exceptions.RequestException:
            return Response(
                text=self.course_error_phrase,
                is_correct=False
            )

    def get_weather_now(self, **kwargs):
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

        city = self.city if kwargs["info"] is None else kwargs["info"]

        try:
            r = requests.get(
                url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric",
                timeout=1
            )

            data = r.json()
            if data["cod"] == "404":
                return Response(
                    header=self.weather_not_found_phrase,
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
                result = f"Погода в городе { city.title() }. \n"
                weather_state = get_translation()
                if weather_state is not None:
                    result += weather_state

                temp1 = cur_weather if self.weather_celsium else int(cur_weather * 9 / 5) + 32
                temp1_pf = " " + declension(temp1, 'фаренгейт')
                result += (f"Температура: {'+' if temp1 > 0 else ''}{ temp1 }"
                           f"{'°' if self.weather_celsium else temp1_pf} \n")

                temp2 = feel if self.weather_celsium else int(feel * 9 / 5) + 32
                temp2_pf = " " + declension(temp2, 'фаренгейт')
                result += (f"Ощущается как {'+' if temp2 > 0 else ''}{ temp2 }"
                           f"{'°' if self.weather_celsium else temp2_pf} \n")

                result += f"Влажность: { humidity }% \n"

                prs = int(pressure * 3 / 4) if self.weather_mmHg else pressure
                prs_phrase = f"милли{ declension(prs, 'метр') } ртутного столба" if self.weather_mmHg \
                    else f"гекто{ declension(prs, 'паскаль')}"

                result += f"Давление: { prs } { prs_phrase } \n"
                result += f"Ветер: { wind } { declension(wind, 'метр') } в секунду."

                return result

            return Response(
                text=prepare_result()
            )
        except requests.exceptions.RequestException:
            return Response(
                text=self.weather_error_phrase,
                is_correct=False
            )
