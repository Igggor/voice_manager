from Sreda.static.metaclasses import SingletonMetaclass


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

        # При изменении имени вызвать build_alias()
        self.NAME = "Среда"

        self.CITY = "Пушкино"

        self.recognizer_threshold = 0.5
        self.microphone_duration = 1
        self.microphone_timeout = 2
        self.phrase_timeout = 10

        # 'en', 'es', 'fr', 'pt', 'de', 'ru' ONLY.
        # SOME FUNCTIONS IN OTHER LANGUAGES ARE NOT AVAILABLE
        self.language_listen = "ru"

        # AVAILABLE EVERYTHING (FROM CONSTANTS.LANGUAGES)
        self.language_speak = "ru"

        self.speak_speed = 1.0

        self.translation_timeout = 4.0
        self.notifications_accuracy = 5.0

        self.weather_celsius = True
        self.weather_mmHg = True

        self.logs_limit = 250
        self.notifications_limit = 15
        self.timers_limit = 50
        self.scenarios_limit = 50
        self.TODO_limit = 50

        self.SCENARIOS = dict()
        self.LOGS = list()
        self.NOTIFICATIONS = list()
        self.TIMERS = list()
        self.TODO_LIST = list()
