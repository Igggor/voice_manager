from TextProcessor import *
from SpeechTranslator import *
from Functions import *
from GlobalContext import *

import sys


class VoiceHelper:
    """
    Главный класс, отвечающий за связь всех элементов приложения
    Singleton - pattern
    """
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(VoiceHelper, cls).__new__(cls)
        return cls.__instance

    # В РАЗРАБОТКЕ, все функции помощника должны быть здесь.
    def __init__(self):
        """
        Конструктор класса.

        Инициализируются все составные части приложения (классы), а также словарь functions, где в качестве значений
        хранятся функции из файла Functions.py
        """
        self.global_context = GlobalContext()
        self.text_processor = TextProcessor(self.global_context)
        self.speech_translator = SpeechTranslator(self.global_context)

        # self.functions хранит ключи, по которым можно обратиться к самой функции ("function") и её аргументам,
        # зависящим от глобальных настроек ("static-args").
        self.functions = {
            "С-N-F":  # воспроизведение фразы, соответствующей состоянию 404
            {
                "function": lambda: self.global_context.RECOGNITION_ERROR_PHRASE,
                "static-args": dict()
            },
            "on":  # включить
            {
                "function": self.set_ON,
                "static-args": dict()
            },
            "off":  # выключить (но оставить чувствительной к команде включения, т.е приложение остается действующим)
            {
                "function": self.set_OFF,
                "static-args": dict()
            },
            "full-off":  # Деактивация, закрытие приложения
            {
                "function": self.exit,
                "static-args": dict()
            },
            "time":  # текущее время
            {
                "function": get_time_now,
                "static-args": dict()
            },
            "date":  # текущая дата
            {
                "function": get_date,
                "static-args": dict()
            },
            "course":  # курс валют
            {
                "function": get_currency_course,
                "static-args": dict()
            },
            "weather-now": {  # текущая погода
                "function": get_weather_now,
                "static-args": dict()
            }
        }

        self.update_args()

    # В перспективе будет вызываться при каждом изменении настроек помощника. Это будет гарантировать актуальность
    # аргументов функции, а значит корректность их работы.
    def update_args(self):
        """
        Обновление аргументов функций голосового помощника, задаваемые настройками.

        :return:
        """
        self.functions["course"]["static-args"] = {
            "__error_phrase": self.global_context.REQUEST_ERROR_PHRASE
        }
        self.functions["weather-now"]["static-args"] = {
            "celsium": self.global_context.weather_temp_celsium,
            "mmHg": self.global_context.weather_pressure_mmHg,
            "__error_phrase": self.global_context.REQUEST_ERROR_PHRASE
        }

    def set_ON(self, **kwargs):
        """
        Включение голосового помощника.

        :return:
        """
        if self.global_context.ON:
            return

        self.speak(self.global_context.GREETING_PHRASE)
        self.global_context.ON = True

    def set_OFF(self, **kwargs):
        """
        Частичное выключение голосового помощника (спящий режим).

        :return:
        """
        if not self.global_context.ON:
            return

        self.speak(self.global_context.BYE_PHRASE)
        self.global_context.ON = False

    # Важно! В перспективе здесь не только выход, но, возможно, какое-то сохранение в БД или что-то подобное.
    def exit(self, **kwargs):
        """
        Полное выключение голосового помощника.

        :return:
        """
        self.global_context.ON = False
        sys.exit()

        pass

    def listen_command(self):
        """
        Объединение несколько функций и методов. Выполнение работы от приёма и расшифровки голоса до непосредственного
        выполнения требуемой функции.

        :return:
        """
        recognized_query = self.speech_translator.listen_command()

        if recognized_query is None:
            return

        print(recognized_query)

        selected_action, additive = self.text_processor.match_command(recognized_query, not self.global_context.ON)
        if selected_action is None:
            return

        self.speak(self.functions[selected_action]["function"](
            **self.functions[selected_action]["static-args"],
            info=additive
        ))

    # В перспективе здесь должно быть собрано несколько функций, в том числе запись логов.
    def speak(self, output_text: str):
        """
        Объединение несколько функций и методов. Выполнение работы от записи логов (not implemented) до
        непосредственного воспроизведения текста.

        :return:
        """
        self.speech_translator.speak(output_text)
