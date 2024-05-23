from dotenv import load_dotenv
import os
import sys


class Environment:
    __ROOT__ = os.path.dirname(__file__)

    MODEL = None
    OPEN_WEATHER_API_KEY = None
    NATIVE_API_KEY = None
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

        if "NATIVE_API_KEY" not in os.environ.keys():
            raise EnvironmentError("Cannot load <NATIVE_API_KEY> from environment: "
                                   "please set-up `.env` file correctly.")
        else:
            Environment.NATIVE_API_KEY = os.environ.get("NATIVE_API_KEY")

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


def build_PYTHONPATH() -> None:
    """
    Метод изменения ``PYTHONPATH`` для корректной работы при запуске из консоли.

    :return:
    """

    path = os.path.dirname(__file__)
    sub_path = os.path.dirname(path)

    if sub_path not in sys.path:
        sys.path.insert(0, sub_path)


def check_model() -> None:
    path = os.path.join(os.path.dirname(__file__), f"model/{Environment.MODEL}.pt")

    if not os.path.exists(path):
        raise ImportError(f"Cannot find whisper-model <{Environment.MODEL}> on path {path}: "
                          f"you should pre-install it. Please run the setup-script 'setup.py' and try again.")