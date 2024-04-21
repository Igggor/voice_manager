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
            * ``text``: текст ответа.
        Опциональные аргументы:
            * ``header``: заголовок ответа [по умолчанию = ``None``];
            * ``is_correct``: корректно ли (без ошибки) завершилась функция [по умолчанию = ``True``];
            * ``type``: тип ответа [по умолчанию = ``None``];
            * ``called_by``: родительская функция [по умолчанию = ``None``];
            * ``do_next``: функции (без аргументов), выполняемые автоматически сразу после ответа.

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
        """
        Получение фразы из экземпляра класса.

        :return: Список из частей фраз (блоков).
            Каждый блок является смысловым предложением, чтобы при остановке воспроизведения не произходило
            заметного разрыва фразы.
        """

        if self.type == "city-not-found-error":
            return self.header + "\n" + "Распознанный город: " + self.text.title() + "."
        if self.type == "format-error":
            return self.header + self.called_by.name.lower() + "." + "\n" + self.text
        if self.type == "notification":
            return self.header + "\n" + "Текст напоминания: " + self.text + "."
        if self.header is not None:
            return self.header + '\n' + self.text

        return self.text


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
            Время воспроизведения уведомления:
                * ``hour``: час;
                * ``hour``: минута.
        Опциональные аргументы:
            * ``second``: секунда [по умолчанию = ``0``].

        :return:
        """

        self.text = kwargs["text"]
        self.id = kwargs["id"]

        self.hour = kwargs["hour"]
        self.minute = kwargs["minute"]
        self.second = 0 if "second" not in kwargs.keys() else kwargs["second"]

        self.previous_check = None

    def check_corresponding(self, current_hour: int, current_minute: int, current_second: int):
        """
        Метод проверки на необходимость воспроизведения данного уведомления прямо сейчас (проверка на то, что его
        время настало).

        :param current_hour: ``int``: текущее время (час);
        :param current_minute: ``int``: текущее время (минута);
        :param current_second: ``int``: текущее время (секунда);

        :return: ``True`` или ``False``.
        """

        def in_segment():
            """
            Проверяет, входит ли время текущего уведомления в отрезок от прошлой проверки до текущего времени.

            :return: ``True`` или ``False``.
            """

            if self.previous_check is None:
                return False

            if self.previous_check["hour"] <= self.hour <= current_hour \
                    and self.previous_check["minute"] <= self.minute <= current_minute \
                    and self.previous_check["second"] <= self.second <= current_second:
                print("FOUND")
                return True
            else:
                return False

        result = in_segment()

        print(self.previous_check)
        print(self.hour, self.minute, self.second)
        print(current_hour, current_minute, current_second)
        print(result)

        if not result:
            self.previous_check = {
                "hour": current_hour,
                "minute": current_minute,
                "second": current_second
            }
        else:
            self.previous_check = None

        return result

    def call(self):
        """
        Вызов уведомления.

        :return: Уведомление, упакованное в класс ``Response``.
        """

        return Response(
            header=f"Напоминание (порядковый номер {self.id}).",
            text=self.text,
            type="notification"
        )
