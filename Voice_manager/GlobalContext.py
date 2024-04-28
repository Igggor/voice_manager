from Metaclasses import SingletonMetaclass
from Units import Response


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

        self.recognizer_threshold = 0.5
        self.microphone_duration = 0.5
        self.microphone_timeout = 2
        self.phrase_timeout = 5
        self.language_listen = "ru-RU"
        self.language_speak = "ru"
        self.speak_speed = 1.0

        self.weather_celsium = True
        self.weather_mmHg = True

        self.logs_limit = 250
        self.notifications_limit = 15
        self.timers_limit = 10
        self.notifications_accuracy = 5

        self.SCENARIOS = dict()
        self.LOGS = list()
        self.NOTIFICATIONS = list()
        self.TIMERS = list()

        self.greeting = Response(
            text=(f"Приветствую, я твой универсальный голосовой помощник {self.NAME}.\n"
                  f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                  f"{self.NAME}, что ты умеешь?")
        )
        self.features = Response(
            text=("Сейчас я мало что умею, да и понимаю человека с трудом. "
                  "Но обещаю, буквально через месяц я смогу очень многое!")
        )

        self.thanks = [
            Response(
                text="Я всегда к вашим услугам."
            ),
            Response(
                text="Всегда пожалуйста!"
            ),
            Response(
                text="Рада стараться."
            )
        ]
        self.small_bye = Response(
            text="Была рада помочь."
        )
        self.big_bye = Response(
            text="Всего доброго, буду рада быть полезной снова."
        )

        self.scenario_creation_success = Response(
            text=(f"Сценарий успешно создан. \n"
                  f"Вы можете запустить его, сказав: {self.NAME}, запусти сценарий "),
        )
        self.scenario_deletion_success = Response(
            text="Сценарий успешно удалён."
        )
        self.note_creation_success = Response(
            text="Напоминание успешно создано. \n"
        )
        self.timer_creation_success = Response(
            text="Таймер успешно создан. \n"
        )
        self.note_deletion_success = Response(
            text="Напоминание успешно удалено. Первое из оставшихся уведомлений теперь имеет номер 1."
        )

        self.recognition_error = Response(
            text="Команда не распознана",
            error=True
        )
        self.weather_request_error = Response(
            text=("Извините, во время получения данных о погоде произошла непредвиденная ошибка. \n"
                  "Повторите запрос позднее."),
            error=True
        )
        self.course_request_error = Response(
            text=("Извините, во время получения данных о курсе валют произошла непредвиденная ошибка. \n"
                  "Повторите запрос позднее."),
            error=True
        )
        self.weather_not_found_error = Response(
            text="Извините, информация о погоде в заданном городе не найдена. Уточните запрос.",
            error=True
        )
        self.wrong_command_format_error = Response(
            text="Неправильный формат запрашиваемой команды: ",
            error=True
        )
        self.scenario_already_exists_error = Response(
            text=(f"Сценарий с данным именем уже существует. \n"
                  f"Попробуйте изменить имя создаваемого сценария. \n"
                  f"Также Вы можете удалить старый сценарий, сказав: {self.NAME}, удали сценарий."),
            error=True
        )
        self.scenario_not_found_error = Response(
            text=("Запрошенный сценарий не найден. \n"
                  "Уточните команду и повторите попытку."),
            error=True
        )
        self.note_not_found_error = Response(
            text=("Не удалось удалить напоминание с заданным порядковым номером.\n"
                  "Похоже, такого напоминания не существует. Уточните команду и повторите попытку."),
            error=True
        )
        self.notes_list_empty_error = Response(
            text="Невозможно найти ближайшее напоминание: список уведомлений пуст.",
            error=True
        )
        self.notes_list_overflow_error = Response(
            text=f"Достигнут лимит количества напоминаний. \n"
                 f"Вы можете увеличить его в настройках или удалить произвольное напоминание, сказав: "
                 f"{self.NAME}, удали напоминание. \n"
                 f"Не забудьте указать номер удаляемого напоминания.",
            error=True
        )
        self.timers_list_overflow_error = Response(
            text="Достигнут лимит количества установленных таймеров. \n"
                 "Вы можете увеличить его в настройках.",
            error=True
        )

    def update_settings(self):
        self.greeting = Response(
            text=(f"Приветствую, я твой универсальный голосовой помощник {self.NAME}.\n"
                  f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                  f"{self.NAME}, что ты умеешь?")
        )

        self.scenario_creation_success = Response(
            text=(f"Сценарий успешно создан. \n"
                  f"Вы можете запустить его, сказав: {self.NAME}, запусти сценарий "),
        )

        self.scenario_already_exists_error = Response(
            text=(f"Сценарий с данным именем уже существует. \n"
                  f"Попробуйте изменить имя создаваемого сценария. \n"
                  f"Также Вы можете удалить старый сценарий, сказав: {self.NAME}, удали сценарий."),
            error=True
        )

        self.notes_list_overflow_error = Response(
            text=f"Достигнут лимит количества напоминаний. \n"
                 f"Вы можете увеличить его в настройках или удалить произвольное напоминание, сказав: "
                 f"{self.NAME}, удали напоминание. \n"
                 f"Не забудьте указать номер удаляемого напоминания.",
            error=True
        )

