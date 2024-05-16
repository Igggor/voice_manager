class Command:
    """
    Структура команды (запроса к голосовому помощнику).
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Инициализирует имя команды, её описание, функцию для исполнения, доп. информацию к запросу,
        а также подкоманды (специально для сценариев).

        Обязательные агрументы:
            * ``name``: имя команды;
            * ``function``: исполняемая функция;
            * ``type``: тип команды;
            * ``key``: ключ команды.
        Опциональные аргументы:
            * ``description``: описание команды [по умолчанию = ``None``];
            * ``triggers``: ключевые слова для вызова команды [по умолчанию - пустой список];
            * ``required_params``: список из необходимых параметров для данной команды [по умолчанию - пустой список];
            * ``ignore_following``: игнорируются ли последующие команды после данной [по умолчанию = ``False``].
            * ``numeric_required``: требуется ли работа с числами [по умолчанию = ``False``].

        :return:
        """

        self.name = kwargs["name"]
        self.description = None if "description" not in kwargs.keys() else kwargs["description"]
        self.key = kwargs["key"]
        self.function = kwargs["function"]
        self.triggers = list() if "triggers" not in kwargs.keys() else kwargs["triggers"]
        self.type = kwargs["type"]

        self.required_params = list() if "required_params" not in kwargs.keys() else kwargs["required_params"]
        self.ignore_following = False if "ignore_following" not in kwargs.keys() else kwargs["ignore_following"]
        self.numeric_required = False if "numeric_required" not in kwargs.keys() else kwargs["numeric_required"]

        self.additive = {
            "main": None
        }


class Response:
    """
    Структура ответа на запрос.
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Инициализирует тип ответа, текст ответа и уточняющую информацию.

        Обязательные агрументы:
            * ``text``: текст ответа.
        Опциональные аргументы:
            * ``info``: доп. информация (в основном, для ошибок) [по умолчанию = ``None``];
            * ``error``: завершилась ли функция с ошибкой [по умолчанию = ``False``];
            * ``called_by``: родительская функция [по умолчанию = ``None``];
            * ``do_next``: функции (без аргументов), выполняемые автоматически сразу после ответа;
            * ``extend_lang``: код используемого языка, помимо русского [по умолчанию = ``None``].

        :return:
        """

        self.text = kwargs["text"]
        self.info = None if "info" not in kwargs.keys() else kwargs["info"]
        self.error = False if "error" not in kwargs.keys() else kwargs["error"]
        self.do_next = None if "do_next" not in kwargs.keys() else kwargs["do_next"]
        self.called_by = None if "called_by" not in kwargs.keys() else kwargs["called_by"]
        self.extend_lang = None if "extend_lang" not in kwargs.keys() else kwargs["extend_lang"]

    def get_speech(self) -> str:
        """
        Получение фразы из экземпляра класса.

        :return: Сама фраза в строковом формате.
        """

        return self.text + (self.info if self.info is not None else "")

    def get_language(self, _undefined: str) -> str:
        """
        Получение доп. языка воспроизведения текста.

        :param _undefined: ``str``: код языка по умолчанию, который будет возвращён, если язык текста не задан явно.

        :return: Язык, на котором будет воспроизведен доп. текст (``info``), если он задан явно, или ``__undefined``.
        """

        return _undefined if self.extend_lang is None else self.extend_lang
