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

        self.recognizer_threshold = 0.5
        self.microphone_duration = 0.5
        self.language_listen = "ru-RU"
        self.language_speak = "ru"

        self.GREETING_PHRASE = (f"Приветствую, я твой универсальный помощник { self.NAME }. "
                                f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                                f"{ self.NAME }, что ты умеешь?")
        self.BYE_PHRASE = "Всего доброго, была рада помочь."
        self.RECOGNITION_ERROR_PHRASE = "Команда не распознана"
