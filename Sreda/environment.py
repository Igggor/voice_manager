from dotenv import load_dotenv
import os
import sys


class Environment:
    __ROOT__ = os.path.dirname(__file__)

    MODEL = None

    OPEN_WEATHER_API_KEY = None
    NATIVE_API_KEY = None
    RECOGNITION_API_KEY = None

    SELF_CODE = None

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
            raise EnvironmentError("Cannot load <MODEL> from environment: "
                                   "please set-up `.env` file correctly.")
        else:
            _AVAILABLE_MODELS = ["nova-2", "base", "whisper-tiny", "whisper-base", "whisper-small", "whisper-medium"]
            MODEL = os.environ.get("MODEL").lower()

            if MODEL not in _AVAILABLE_MODELS:
                raise EnvironmentError(f"No such model: <{MODEL.lower()}. Available models: {_AVAILABLE_MODELS}")
            else:
                Environment.MODEL = MODEL

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

        if "RECOGNITION_API_KEY" not in os.environ.keys():
            raise EnvironmentError("Cannot load <RECOGNITION_API_KEY> from environment: "
                                   "please set-up `.env` file correctly.")
        else:
            Environment.RECOGNITION_API_KEY = os.environ.get("RECOGNITION_API_KEY")

        if "SELF_CODE" not in os.environ.keys():
            raise EnvironmentError("Cannot load <SELF_CODE> from environment: "
                                   "please set-up `.env` file correctly.")
        else:
            Environment.SELF_CODE = os.environ.get("SELF_CODE")

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
