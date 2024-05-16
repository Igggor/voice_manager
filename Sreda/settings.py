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

        # При изменении имени вызвать build_alias()
        self.NAME = ["Среда"]

        self.CITY = "Пушкино"

        self.OPEN_WEATHER_API_KEY = None

        self.recognizer_threshold = 0.5
        self.microphone_duration = 0.5
        self.microphone_timeout = 2
        self.phrase_timeout = 5

        # 'en', 'es', 'fr', 'pt', 'de', 'ru' ONLY.
        # SOME FUNCTIONS IN OTHER LANGUAGES ARE NOT AVAILABLE
        self.language_listen = "en"

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


class Environment:
    __ROOT__ = os.path.dirname(__file__)

    MODEL = None
    OPEN_WEATHER_API_KEY = None
    DYNAMIC_BUILDING = None


def load_environment() -> None:
    """
    Загрузка переменных из окружения ``.env``.

    :return:
    """

    dotenv_path = os.path.join(os.path.dirname(__file__), "storage/.env")

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

        if "MODEL" not in os.environ.keys():
            raise EnvironmentError("Cannot load <MODEL> from environment: please set-up `.env` file correctly.")
        else:
            _AVAILABLE_MODELS = ["tiny", "base", "small"]
            MODEL = os.environ.get("MODEL")

            if MODEL.lower() in _AVAILABLE_MODELS:
                Environment.MODEL = MODEL.lower()
            else:
                raise EnvironmentError(f"Cannot load <MODEL> from environment: incorrect value. "
                                       f"Available values: {_AVAILABLE_MODELS}.")

        if "WEATHER_API_KEY" not in os.environ.keys():
            raise EnvironmentError("Cannot load <WEATHER_API_KEY> from environment: "
                                   "please set-up `.env` file correctly.")
        else:
            Environment.OPEN_WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

        if "DYNAMIC_BUILDING" not in os.environ.keys():
            raise EnvironmentError("Cannot load <DYNAMIC_BUILDING> from environment: "
                                   "please set-up `.env` file correctly.")
        else:
            DYNAMIC_BUILDING = os.environ.get("DYNAMIC_BUILDING")
            if DYNAMIC_BUILDING.lower() == "true":
                Environment.DYNAMIC_BUILDING = True
            elif DYNAMIC_BUILDING.lower() == "false":
                Environment.DYNAMIC_BUILDING = False
            else:
                raise EnvironmentError(f"Cannot load <DYNAMIC_BUILDING> from environment: incorrect value. "
                                       f"Available values: 'True' or 'False'.")
    else:
        raise FileNotFoundError("Cannot find `.env` file on path Sreda/storage/.env "
                                "with expected attributes <MODEL>, <WEATHER_API_KEY>, <DYNAMIC_BUILDING>.")


def check_model() -> None:
    path = os.path.join(os.path.dirname(__file__), f"model/{Environment.MODEL}.pt")

    if not os.path.exists(path):
        raise ImportError(f"Cannot find whisper-model <{Environment.MODEL}> on path Sreda/model: "
                          f"you should pre-install it. Please run the setup-script 'setup.py' and try again.")
