from datetime import datetime


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
            * ``key``: ключ команды
        Опциональные аргументы:
            * ``description``: описание команды [по умолчанию = ``None``];
            * ``triggers``: ключевые слова для вызова команды [по умолчанию - пустой список];
            * ``additive_required``: обязательна ли доп. информация к команде [по умолчанию = ``False``];
            * ``subcommands_required``: необходимы ли подкоманды [по умолчанию = ``False``].

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
            * ``do_next``: функции (без аргументов), выполняемые автоматически сразу после ответа.

        :return:
        """

        self.text = kwargs["text"]
        self.info = None if "info" not in kwargs.keys() else kwargs["info"]
        self.error = False if "error" not in kwargs.keys() else kwargs["error"]
        self.do_next = None if "do_next" not in kwargs.keys() else kwargs["do_next"]
        self.called_by = None if "called_by" not in kwargs.keys() else kwargs["called_by"]

    def get_speech(self):
        """
        Получение фразы из экземпляра класса.

        :return: Сама фраза в строковом формате.
        """

        return self.text + (self.info if self.info is not None else "")


class PlayableText:
    """
    Обертка воспроизводимого текста для многофункциональной работы с ним.
    """

    def __init__(self):
        self.blocks = list()

    def add(self, text: str):
        """
        Добавление текста к воспроизводимой фразе.

        :param text: ``str``: добавляемый текст.

        :return:
        """

        blocks = text.split('\n')
        self.join_blocks(blocks)

    def join_blocks(self, blocks: list):
        """
        Добавление текстового блока к воспроизводимому тексту.

        :param blocks: ``list``: добавляемый текст.

        :return:
        """

        self.blocks.append(list())
        for block in blocks:
            # Empty block
            if not block:
                continue

            self.blocks[len(self.blocks) - 1].append(block)

    def get_normal_text(self):
        """
        Получение нормального текстового представления экземпляра ``PlayableText``.

        :return: Воспроизводимый текст.
        """

        output_text = ""
        for query in self.blocks:
            for block in query:
                output_text += (block + '\n')
            output_text += '\n'

        return output_text

    def get_straight_blocks(self):
        """
        Метод "выпрямления" списка блоков (преобразование из двумерного списка в одномерный).

        :return: Полученный одномерный список фраз.
        """

        output_blocks = list()
        for query in self.blocks:
            for block in query:
                output_blocks.append(block)

        return output_blocks


class Notification:
    """
    Структура уведомения.
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Инициализирует текст уведомления и его время.

        Обязательные агрументы:
            * ``text``: текст уведомления;
            * ``id``: уникальный идентификатор уведомления.
            * ````

        :return:
        """

        self.text = kwargs["text"]
        self.id = kwargs["id"]

        self.hour = kwargs["hour"]
        self.minute = kwargs["minute"]
        self.second = kwargs["second"]
        self.month = kwargs["month"]
        self.day = kwargs["day"]
        self.timer = kwargs["timer"]

        current_time = datetime.now()
        self.previous_check = current_time

    def check_corresponding(self):
        """
        Метод проверки на необходимость воспроизведения данного уведомления прямо сейчас (проверка на то, что его
        время настало).

        :return: ``True`` или ``False``.
        """

        current_time = datetime.now()

        def in_segment():
            """
            Проверяет, входит ли время текущего уведомления в отрезок от прошлой проверки до текущего времени.

            :return: ``True`` или ``False``.
            """

            if self.day is None:
                moment = datetime(year=current_time.year, month=current_time.month, day=current_time.day,
                                  hour=self.hour, minute=self.minute, second=self.second)
            else:
                moment = datetime(year=current_time.year, month=self.month, day=self.day,
                                  hour=self.hour, minute=self.minute, second=self.second)

            if self.previous_check <= moment <= current_time:
                return True

            return False

        result = in_segment()

        self.previous_check = current_time

        return result

    def call(self):
        """
        Вызов уведомления.

        :return: Уведомление, упакованное в класс ``Response``.
        """

        text = "отсутствует (не указан)." if self.text is None else self.text
        if self.timer:
            return Response(
                text=f"Внимание! Таймер! \n",
                info="Текст таймера: " + text,
                type="notification"
            )
        else:
            return Response(
                text=f"Напоминание (порядковый номер {self.id}). \n",
                info="Текст напоминания: " + text,
                type="notification"
            )


class Scenario:
    """
    Структура сценария.
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Обязательные аргументы:
            * ``name``: имя (название) сценария;
            * ``functions``: список команд класса ``Command``, которые нужно исполнить при вызове сценария.

        Инициализирует название сценария, а также команды, которые исполняются при его вызове.

        :return:
        """

        self.name = kwargs["name"]
        self.units = kwargs["functions"]

    def execute_scenario(self):
        """
        Выполнение сценария.

        :return: Возвращает текст результата выполнения команд сценария.
        """

        output_text = f"Исполняю сценарий { self.name }. \n"
        for item in self.units:
            output_text += item.function(**item.additive)

        return Response(
            text=output_text
        )


class TodoUnit:
    """
    Структура элемента списка дел.
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Обязательные аргументы:
            * ``text``: текст элемента;
            * ``category``: категория элемента.
        """

        raise NotImplementedError
