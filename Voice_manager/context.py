from meta import SingletonMetaclass


class GlobalContext(metaclass=SingletonMetaclass):
    """
    Класс глобальных настроек.
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
        self.microphone_timeout = 2
        self.phrase_timeout = 10
        self.language_listen = "ru-RU"
        self.language_speak = "ru"
        self.speak_speed = 1.0

        self.weather_celsium = True
        self.weather_mmHg = True

        self.logs_limit = 250
        self.notifications_limit = 100
        self.notifications_accuracy = 5

        self.SCENARIOS = dict()
        self.LOGS = list()
        self.NOTIFICATIONS = list()
