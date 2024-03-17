class GlobalContext:
    """
    Класс глобальных настроек.
    Singleton - pattern
    """
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GlobalContext, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.ON = False
        self.NAME = "Среда"
        self.CITY = "Пушкино"

        self.recognizer_threshold = 0.5
        self.microphone_duration = 0.5
        self.microphone_timeout = 1
        self.language_listen = "ru-RU"
        self.language_speak = "ru"

        self.weather_temp_celsium = True
        self.weather_pressure_mmHg = True

        self.GREETING_PHRASE = (f"Приветствую, я твой универсальный помощник { self.NAME }. "
                                f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                                f"{ self.NAME }, что ты умеешь?")
        self.BYE_PHRASE = "Всего доброго, была рада помочь."
        self.RECOGNITION_ERROR_PHRASE = "Команда не распознана"
        self.REQUEST_ERROR_PHRASE = ("Извините, во время получения данных произошла непредвиденная ошибка. "
                                     "Повторите запрос позднее.")
