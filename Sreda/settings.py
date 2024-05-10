from Sreda.static.metaclasses import SingletonMetaclass

from dotenv import load_dotenv
import os


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

        self.OPEN_WEATHER_API_KEY = None

        self.recognizer_threshold = 0.5
        self.microphone_duration = 0.5
        self.microphone_timeout = 2
        self.phrase_timeout = 15
        self.language_listen = "ru"
        self.language_speak = "ru"
        self.speak_speed = 1.0

        self.translation_timeout = 4.0
        self.notifications_accuracy = 20.0

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


class Environment:
    __ROOT__ = __file__

    BUILD = True
    OPEN_WEATHER_API_KEY = None


def load_environment() -> None:
    """
    Загрузка переменных из окружения ``.env``.

    :return:
    """

    dotenv_path = os.path.join(os.path.dirname(__file__), "storage/.env")

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

        if "BUILD" not in os.environ.keys():
            print(f"Warning: something went wrong while loading <BUILD> from environment: "
                  f"please set-up `.env` file. <BUILD> now is True.")

            Environment.BUILD = True
        else:
            BUILD = os.environ.get("BUILD")
            if BUILD.lower() == "true" or BUILD == "1":
                Environment.BUILD = True
            elif BUILD.lower() == "false" or BUILD == "0":
                Environment.BUILD = False
            else:
                print(f"Warning: something went wrong while loading <BUILD> from environment: "
                      f"incorrect value. <BUILD> now is True.")

        if "WEATHER_API_KEY" not in os.environ.keys():
            print(f"Warning: something went wrong while loading <WEATHER_API_KEY> from environment: "
                  f"please set-up `.env` file. <WEATHER_API_KEY> isn't set, so the weather request will fail.")

            Environment.OPEN_WEATHER_API_KEY = None
        else:
            Environment.OPEN_WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

    else:
        raise FileNotFoundError("Cannot find `.env` file on path Sreda/storage/.env "
                                "with expected attributes <BUILD>, <WEATHER_API_KEY>.")
