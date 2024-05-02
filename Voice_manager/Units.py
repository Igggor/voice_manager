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
            * ``required_params``: список из необходимых параметров для данной команды [по умолчанию - пустой список];
            * ``ignore_following``: игнорируются ли последующие команды после данной [по умолчанию = ``False``].

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

    def get_speech(self):
        """
        Получение фразы из экземпляра класса.

        :return: Сама фраза в строковом формате.
        """

        return self.text + (self.info if self.info is not None else "")

    def get_language(self, __undefined: str):
        """
        Получение доп. языка воспроизведения текста.

        :param __undefined: ``str``: код языка по умолчанию, который будет возвращён, если язык текста не задан явно.

        :return: Язык, на котором будет воспроизведен доп. текст (``info``), если он задан явно, или ``__undefined``.
        """

        return __undefined if self.extend_lang is None else self.extend_lang


class PlayableText:
    """
    Обертка воспроизводимого текста для многофункциональной работы с ним.

    **Структура:**
        Представляет собой список ``blocks``, причём один элемент соответствует одной команде.

        Элементами являются "непрерывные части" текста одной команды. При переходе от одной такой части к другой
        вопроизведение может быть безопасно прервано.

        "Непрерывные части" состоят из словарей вида:
            ``{source: текст, language: язык текста}``.
    """

    def __init__(self):
        self.blocks = list()

    def add(self, text: str, lang: str, new: bool = True):
        """
        Добавление текста к воспроизводимой фразе.

        :param text: ``str``: добавляемый текст;
        :param lang: ``str``: код языка текста;
        :param new: ``bool`` выделяется ли новый блок под добавляемый текст.

        :return:
        """

        blocks = text.split('\n')

        if new:
            self.blocks.append(list())

        for block in blocks:
            # Empty block
            if not block:
                continue

            self.blocks[len(self.blocks) - 1].append({
                "source": block,
                "language": lang
            })

    def get_normal_text(self):
        """
        Получение текстового представления экземпляра ``PlayableText`` в читабельном виде,
        но не предназначенном для воспроизведения.

        :return: Воспроизводимый текст.
        """

        output_text = ""
        for query in self.blocks:
            for block in query:
                output_text += (block["source"] + '\n')
            output_text += '\n'

        return output_text

    def get_straight_blocks(self):
        """
        Метод "выпрямления" списка блоков (преобразование из двумерного списка в одномерный).

        :return: Полученный одномерный список фраз, представляющих собой тело (сам текст) и код языка воспроизведения.
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
