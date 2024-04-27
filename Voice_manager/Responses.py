from Units import Response
from GlobalContext import GlobalContext


class ResponsesHandler:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ResponsesHandler, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.greeting = None
        self.features = None

        self.thanks = None
        self.small_bye = None
        self.big_bye = None

        self.scenario_creation_success = None
        self.scenario_deletion_success = None
        self.note_creation_success = None
        self.note_deletion_success = None
        self.timer_creation_success = None

        self.recognition_error = None
        self.weather_request_error = None
        self.course_request_error = None
        self.weather_not_found_error = None
        self.wrong_command_format_error = None
        self.scenario_already_exists_error = None
        self.scenario_not_found_error = None
        self.note_not_found_error = None
        self.notes_list_empty_error = None
        self.notes_list_overflow_error = None
        self.timers_list_overflow_error = None

        self.update_settings()

    def update_settings(self):
        global_context = GlobalContext()

        self.greeting = Response(
            text=(f"Приветствую, я твой универсальный голосовой помощник { global_context.NAME }.\n"
                  f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                  f"{ global_context.NAME }, что ты умеешь?")
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
            text=("Сценарий успешно создан. \n"
                  "Вы можете запустить его, сказав: Среда, запусти сценарий "),
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
            text=("Сценарий с данным именем уже существует. \n"
                  "Попробуйте изменить имя создаваемого сценария. \n"
                  "Также Вы можете удалить старый сценарий, сказав: Среда, удали сценарий."),
            error=True
        )
        self.scenario_not_found_error = Response(
            text=("Запрошенный сценарий не найден. \n"
                  "Уточните команду и повторите попытку."),
            error=True
        )
        self.note_not_found_error = Response(
            text=("Не удалось удалить напоминание с заданным порядковым номером.\n"
                  "Уточните команду и повторите попытку."),
            error=True
        )
        self.notes_list_empty_error = Response(
            text="Невозможно найти ближайшее напоминание: список уведомлений пуст.",
            error=True
        )
        self.notes_list_overflow_error = Response(
            text=f"Достигнут лимит количества напоминаний. \n"
                 f"Вы можете увеличить его в настройках или удалить произвольное напоминание, сказав: "
                 f"{ global_context.NAME }, удали напоминание. \n"
                 f"Не забудьте указать номер удаляемого напоминания.",
            error=True
        )
        self.timers_list_overflow_error = Response(
            text="Достигнут лимит количества установленных таймеров. \n"
                 "Вы можете увеличить его в настройках.",
            error=True
        )
