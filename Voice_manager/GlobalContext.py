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
        self.microphone_timeout = 2
        self.phrase_timeout = 10
        self.language_listen = "ru-RU"
        self.language_speak = "ru"
        self.speak_speed = 1.0

        self.weather_temp_celsium = True
        self.weather_pressure_mmHg = True

        self.logs_limit = 250
        self.notifications_limit = 100
        self.notifications_accuracy = 5

        self.SCENARIOS = dict()
        self.LOGS = list()
        self.NOTIFICATIONS = list()

        self.GREETING_PHRASE = (f"Приветствую, я твой универсальный помощник { self.NAME }. \n"
                                f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                                f"{ self.NAME }, что ты умеешь?")
        self.FEATURES_PHRASE = ("Сейчас я мало что умею, да и понимаю человека с трудом. "
                                "Но обещаю, буквально через месяц я смогу очень многое!")
        self.THANKS_PHRASES = ["Я всегда к вашим услугам.", "Всегда пожалуйста!", "Рада стараться."]
        self.SMALL_BYE_PHRASE = "Была рада помочь."
        self.BIG_BYE_PHRASE = "Всего доброго, буду рада быть полезной снова."
        self.RECOGNITION_ERROR_PHRASE = "Команда не распознана"
        self.WEATHER_REQUEST_ERROR_PHRASE = ("Извините, во время получения данных о погоде "
                                             "произошла непредвиденная ошибка. \n"
                                             "Повторите запрос позднее.")
        self.COURSE_REQUEST_ERROR_PHRASE = ("Извините, во время получения данных о курсе валют "
                                            "произошла непредвиденная ошибка. \n"
                                            "Повторите запрос позднее.")
        self.WEATHER_NOT_FOUND_PHRASE = "Извините, информация о погоде в заданном городе не найдена. Уточните запрос."
        self.WRONG_COMMAND_FORMAT_PHRASE = "Неправильный формат запрашиваемой команды: "
        self.SCENARIO_ALREADY_EXISTS_PHRASE = ("Сценарий с данным именем уже существует. \n"
                                               "Попробуйте изменить имя создаваемого сценария. \n"
                                               "Также Вы можете удалить старый сценарий, сказав: "
                                               "Среда, удали сценарий.")
        self.SCENARIO_CREATION_SUCCESS_PHRASE = ("Сценарий успешно создан. \n"
                                                 "Вы можете запустить его, сказав: Среда, запусти сценарий ")
        self.SCENARIO_DELETION_SUCCESS_PHRASE = "Сценарий успешно удалён."
        self.SCENARIO_NOT_FOUND_PHRASE = ("Запрошенный сценарий не найден. \n"
                                          "Уточните команду и повторите попытку.")
        self.NOTIFICATION_CREATION_SUCCESS_PHRASE = "Уведомление успешно создано, оно будет запущено в заданное время."
        self.NOTIFICATION_DELETION_SUCCESS_PHRASE = "Уведомление успешно удалено."
        self.NOTIFICATION_DELETION_FAILED_PHRASE = ("Не удалось удалить уведомление с заданным порядковым номером.\n"
                                                    "Уточните команду и повторите попытку.")
        self.EMPTY_NOTIFICATIONS_ERROR_PHRASE = "Невозможно найти уведомление: список уведомлений пуст."
