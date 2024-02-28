from GlobalContext import *
from TextProcessor import *
from SpeechTranslator import *
from Functions import *

import sys


# Главный класс, отвечающий за связь всех элементов приложения.
# Singleton - pattern
class VoiceHelper:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(VoiceHelper, cls).__new__(cls)
        return cls.__instance

    # Конструктор.
    # Инициализируются все составные части приложения (классы), а также словарь functions, где в качестве значений
    # хранятся функции из файла Functions.py.

    # В РЕЗРАБОТКЕ, все функции помощника должны быть здесь.
    def __init__(self):
        self.globalContext = GlobalContext()
        self.textProcessor = TextProcessor(self.globalContext.NAME)
        self.speechTranslator = SpeechTranslator()

        self.functions = {
            "time": getTimeNow,  # текущее время
            "on": self.setON,  # включить
            "off": self.setOFF,  # выключить (но оставить чувствительной к команде включения,
                                 # т.е приложение остается действующим)
            "full-off": self.exit,  # Деактивация, закрытие приложения
            "date": getDate  # текущая дата
        }

    # Метод.
    # Выполняет включение голосового помощника.
    def setON(self):
        if self.globalContext.ON:
            return

        self.speechTranslator.speak(self.textProcessor.GREETING_PHRASE)
        self.globalContext.ON = True

    # Метод.
    # Выполняет частичное выключение голосового помощника (спящий режим).
    def setOFF(self):
        if not self.globalContext.ON:
            return

        self.speechTranslator.speak(self.textProcessor.BYE_PHRASE)
        self.globalContext.ON = False

    # Метод.
    # Выполняет полное выключение голосового помощника.
    # Важно! В перспективе здесь не только выход, но, возможно, какое-то сохранение в БД или что-то подобное.
    def exit(self):
        self.globalContext.ON = False
        sys.exit()

        pass

    # Метод.
    # Объединяет в себе несколько функций и методов. Выполняет всю работу от приёма и расшифровки голоса до
    # непосредственного выполнения требуемой функции.
    def listenCommand(self):
        recognizedQuery = self.speechTranslator.listenCommand()

        if recognizedQuery is None:
            return

        if recognizedQuery == self.speechTranslator.RECOGNITION_ERROR_PHRASE:
            self.speechTranslator.speak(recognizedQuery)
            return

        selectedActions = self.textProcessor.matchCommand(recognizedQuery, self.globalContext.ON)

        if selectedActions is None:
            return

        for action in selectedActions:
            self.speechTranslator.speak(self.functions[action]())
