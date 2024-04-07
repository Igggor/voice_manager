class GlobalContext:
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
        self.microphone_timeout = 1
        self.language_listen = "ru-RU"
        self.language_speak = "ru"
        self.speak_speed = 1.0

        self.weather_temp_celsium = True
        self.weather_pressure_mmHg = True

        self.GREETING_PHRASE = (f"Приветствую, я твой универсальный помощник { self.NAME }. "
                                f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                                f"{ self.NAME }, что ты умеешь?")
        self.FEATURES_PHRASE = ("Сейчас я мало что умею, да и понимаю человека с трудом. "
                               "Но обещаю, буквально через месяц я смогу очень многое!")
        self.THANKS_PHRASES = ["Я всегда к вашим услугам.", "Всегда пожалуйста!", "Рада стараться."]
        self.BYE_PHRASE = "Всего доброго, была рада помочь."
        self.RECOGNITION_ERROR_PHRASE = "Команда не распознана"
        self.REQUEST_ERROR_PHRASE = ("Извините, во время получения данных произошла непредвиденная ошибка. "
                                     "Повторите запрос позднее.")
        self.NOT_FOUND_PHRASE = "Извините, запрашиваемая информация не найдена. Уточните запрос."
        self.WRONG_COMMAND_FORMAT_PHRASE = "Неправильный формат запрашиваемой команды: "
        self.SCENARIO_ALREADY_EXISTS_PHRASE = ("Сценарий с данным именем уже существует. Попробуйте изменить имя "
                                               "создаваемого или старого сценария. Также Вы можете удалить старый "
                                               "сценарий, сказав: Среда, удали сценарий.")
        self.SCENARIO_CREATION_SUCCESS_PHRASE = ("Сценарий успешно создан. Вы можете запустить его, сказав: "
                                                 "Среда, запусти сценарий ")
        self.SCENARIO_DELETION_SUCCESS_PHRASE = "Сценарий успешно удалён."
        self.SCENARIO_NOT_FOUND_PHRASE = "Запрошенный сценарий не найден. Уточните команду и повторите попытку."
