class Command:
    """
    Структура команды (запроса к голосовому помощнику).
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Инициализирует имя команды, её описание, функцию для исполнения, доп. информацию к запросу,
        постоянные агументы, а также подкоманды (специально для сценариев).

        Обязательные агрументы:
            * ``name``: имя команды;
            * ``function``: исполняемая функция;
            * ``type``: тип команды;
            * ``key``: ключ команды
        Опциональные аргументы:
            * ``description``: описание команды;
            * ``triggers``: ключевые слова для вызова команды;
            * ``additive_required``: обязательна ли доп. информация к команде;
            * ``subcommands_required``: необходимы ли подкоманды.

        :return:
        """

        self.name = kwargs["name"]
        self.description = None if "description" not in kwargs.keys() else kwargs["description"]
        self.key = kwargs["key"]
        self.function = kwargs["function"]
        self.triggers = list() if "triggers" not in kwargs.keys() else kwargs["triggers"]
        self.type = kwargs["type"]

        self.additive_required = False if "additive_required" not in kwargs.keys() else kwargs["additive_required"]
        self.subcommands_required = False if "subcommands_required" not in kwargs.keys() else (
            kwargs["subcommands_required"])

        self.additive = None
        self.subcommands = list()


class Response:
    """
    Структура ответа на запрос.
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Инициализирует тип ответа, текст ответа и уточняющую информацию.

        Обязательные агрументы:
            * ``text``: текст ответа. Необязателен, только если ``skipped`` = True.
        Опциональные аргументы:
            * ``header``: заголовок ответа;
            * ``is_correct``: корректно ли (без ошибки) завершилась функция;
            * ``type``: тип ответа;
            * ``called_by``: родительская функция;
            * ``do_next``: сопутствующая функции, выполняемые автоматически сразу после ответа.
            Не должны содержать аргументов.

        :return:
        """

        self.text = None
        self.header = None
        self.called_by = None
        self.is_correct = None
        self.type = None

        self.text = kwargs["text"]
        self.header = None if "header" not in kwargs.keys() else kwargs["header"]
        self.called_by = None if "called_by" not in kwargs.keys() else kwargs["called_by"]
        self.is_correct = True if "is_correct" not in kwargs.keys() else kwargs["is_correct"]
        self.type = None if "type" not in kwargs.keys() else kwargs["type"]
        self.do_next = None if "do_next" not in kwargs.keys() else kwargs["do_next"]

    def get_speech(self):
        if self.type == "city-not-found-error":
            return self.header + '\n' + "Распознанный город: " + self.text + '.'
        if self.type == "format-error":
            return self.header + self.called_by.name.lower() + ". " + self.text

        return self.text
