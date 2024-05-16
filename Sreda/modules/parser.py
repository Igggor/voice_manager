import datetime

from Sreda.modules.text.units import Command

from Sreda.static.local import get_month, get_language_key, get_word

from string import punctuation


def remove_whitespaces(text: str) -> str | None:
    """
    Удаляет из строки лишние пробелы.

    :param text: ``str``: строка.

    :return: Очищенная строка.
    """

    if text is None:
        return None

    cleared = str()
    previous_char = " "

    for char in text:
        if char == " " and previous_char == " ":
            continue

        cleared += char
        previous_char = char

    return cleared


def canonize_text(text: str) -> str:
    """
    Удаляет из строки лишние пробелы, знаки препинания, делает ``lowercase``.

    :param text: ``str``: строка.

    :return: Очищенная строка.
    """

    punctuation_sieve = str.maketrans("", "", punctuation)

    text = text.lower()
    text = remove_whitespaces(text=text)
    text = text.translate(punctuation_sieve)

    return text


def _parse_time(text: str, lang: str) -> dict[str, int] | None:
    """
    Выделяет из строки время.

    :param text: ``str``: строка, из которой необходимо выделить время;
    :param lang: ``str``: язык.

    :return: Словарь с полями ``hours``, ``minutes``, ``seconds`` в случае,
        если в строке успешно найдены данные времени. В противном случае будет возвращено ``None``.
    """

    hours = 0
    minutes = 0
    seconds = 0

    hours_filled = False
    minutes_filled = False
    seconds_filled = False

    units = text.split()

    if not len(units):
        return None

    if units[0] == get_word(text="на", lang=lang):
        del units[0]

    for i in range(len(units)):
        unit = units[i]

        if unit.isdigit():
            if i + 1 >= len(units):
                break

            next_unit = units[i + 1]
            if next_unit.isdigit():
                return None

            if next_unit == get_word(text="час", lang=lang) or next_unit == get_word(text="часов", lang=lang) or \
                    next_unit == get_word(text="часа", lang=lang):
                if hours_filled:
                    return None

                hours = int(unit)
                hours_filled = True
                continue
            elif next_unit == get_word(text="минута", lang=lang) or next_unit == get_word(text="минут", lang=lang) or \
                    next_unit == get_word(text="минуты", lang=lang):
                if minutes_filled:
                    return None

                minutes = int(unit)
                minutes_filled = True
                continue
            elif next_unit == get_word(text="секунда", lang=lang) or next_unit == get_word(text="секунд", lang=lang) \
                    or next_unit == get_word(text="секунды", lang=lang):
                if seconds_filled:
                    return None

                seconds = int(unit)
                seconds_filled = True
                continue

            return None
        else:
            continue

    if not hours_filled and not minutes_filled and not seconds_filled:
        return None

    response = {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

    print('[Log: time_parse]: ', response)
    return response


def _parse_date(text: str, lang: str, light: bool = False) -> dict[str, int] | None:
    """
    Выделяет из строки дату.

    :param text: ``str``: строка, из которой необходимо выделить дату;
    :param lang: ``str``: язык.

    :return: Словарь с полями ``month``, ``day`` в случае,
        если в строке успешно найдена дата. В противном случае будет возвращено ``None``.
    """

    units = text.split()

    if not len(units):
        return None

    if units[0] == get_word(text="на", lang=lang):
        del units[0]

    if len(units) == 1:
        today = datetime.datetime.today()
        if units[0] == get_word(text="сегодня", lang=lang):
            response = {
                "today": True,
                "day": today.day,
                "month": today.month
            }

            return response
        if units[0] == get_word(text="завтра", lang=lang):
            tomorrow = today + datetime.timedelta(days=1)
            response = {
                "day": tomorrow.day,
                "month": tomorrow.month
            }

            return response

    for i in range(len(units)):
        unit = units[i]

        int_unit = int(unit[:len(unit) - 2]) if unit[:len(unit) - 2].isdigit() else \
            int(unit) if unit.isdigit() else None

        if int_unit is not None:
            if i + 1 >= len(units):
                break

            next_unit = units[i + 1]

            base = get_month(next_unit, lang=lang)
            if base is None:
                continue

            day = int_unit
            month = base

            response = {
                "day": day,
                "month": month
            }

            return response

    if light:
        if len(units) != 1:
            return None

        month = get_month(units[0], i=True, lang=lang)
        if month is not None:
            response = {
                "day": None,
                "month": month
            }

            return response

    return None


def _parse_notification_creation(command: Command, lang: str) -> None:
    """
    Обрабатывает команду добавления напоминания / таймера.

    :param command: ``Command``: обрабатываемая команда. **Изменяется внутри функции**;
    :param lang: ``str``: язык.

    :return:
    """

    additive = command.additive["main"]
    if additive is None:
        return

    words = additive.split()

    date = list()
    time = list()
    text = list()

    key = -1
    operational = [
        {
            "keys": [get_word(text="текст", lang=lang)],
            "source": text
        },
        {
            "keys": [get_word(text="дата", lang=lang)],
            "source": date
        },
        {
            "keys": [get_word(text="время", lang=lang)],
            "source": time
        }
    ]

    for word in words:
        if key == 0:
            text.append(word)
            continue

        skip = False
        for index in range(len(operational)):
            if word in operational[index]["keys"]:
                key = index
                skip = True
                break

        if skip or key == -1:
            continue

        operational[key]["source"].append(word)

    time_response = _parse_time(' '.join(time), lang=lang)
    date_response = _parse_date(' '.join(date), lang=lang)
    text_response = None if len(text) == 0 else ' '.join(text)

    command.additive["main"] = text_response
    command.additive["time"] = time_response

    if command.key == "add-notification":
        command.additive["date"] = date_response


def _parse_translation(command: Command, lang: str) -> None:
    """
    Обрабатывает команду перевода текста.

    :param command: ``Command``: обрабатываемая команда. **Изменяется внутри функции**.

    :return:
    """

    words = command.additive["main"].split()

    text = list()
    language = list()

    key = 1
    operational = [
        {
            "keys": [get_word(text="текст", lang=lang)],
            "source": text
        },
        {
            "keys": [get_word(text="язык", lang=lang)],
            "source": language
        }
    ]

    for word in words:
        if key == 0:
            text.append(word)
            continue

        skip = False
        for index in range(len(operational)):
            if word in operational[index]["keys"]:
                key = index
                skip = True
                break

        if skip or key == -1:
            continue

        operational[key]["source"].append(word)

    if len(language) and language[0] == get_word(text="на", lang=lang):
        del language[0]

    command.additive = {
        "main": ' '.join(text),
        "language": get_language_key(' '.join(language), lang=lang)
    }


def _parse_TODO_creation(command: Command, lang: str) -> None:
    """
    Обрабатывает команду добавления заметки.

    :param command: ``Command``: обрабатываемая команда. **Изменяется внутри функции**;
    :param lang: ``str``: язык.

    :return:
    """

    additive = command.additive["main"]
    if additive is None:
        return

    words = additive.split()

    date = list()
    text = list()

    key = 1
    operational = [
        {
            "keys": [get_word(text="текст", lang=lang)],
            "source": text
        },
        {
            "keys": [get_word(text="дата", lang=lang)],
            "source": date
        }
    ]

    for word in words:
        if key == 0:
            text.append(word)
            continue

        skip = False
        for index in range(len(operational)):
            if word in operational[index]["keys"]:
                key = index
                skip = True
                break

        if skip or key == -1:
            continue

        operational[key]["source"].append(word)

    date_response = _parse_date(' '.join(date), lang=lang)
    text_response = None if len(text) == 0 else ' '.join(text)

    command.additive["main"] = text_response
    command.additive["date"] = date_response


def _parse_TODO_find(command: Command, lang: str):
    """
        Обрабатывает команду добавления заметки.

        :param command: ``Command``: обрабатываемая команда. **Изменяется внутри функции**;
        :param lang: ``str``: язык.

        :return:
        """

    additive = command.additive["main"]
    if additive is None:
        return

    date_response = _parse_date(additive, lang=lang, light=True)

    command.additive["date"] = date_response


def parse_info(command: Command, lang: str) -> Command:
    """
    Обрабатывает ``additive`` (дополнительную информацию) переданной команды.

    :param command: ``Command``: обрабатываемая команда;
    :param lang: ``str``: язык.

    :return: Возвращает экземпляр класса ``Command`` - обработанную команду.
    """

    if command.additive["main"] is None:
        return command

    print("[Log: parse]: " + command.additive["main"])

    if command.type == "notification-adding":
        _parse_notification_creation(command=command, lang=lang)

    if command.key == "delete-notification":
        command.additive["main"] = command.additive["main"].replace(get_word(text="порядковый", lang=lang), "")
        command.additive["main"] = command.additive["main"].replace(get_word(text="номер", lang=lang), "")

    if command.key == "translate":
        _parse_translation(command=command, lang=lang)

    if command.key == "add-TODO":
        _parse_TODO_creation(command=command, lang=lang)

    if command.key == "find-TODO":
        command.additive["main"] = command.additive["main"].replace(get_word(text="дата", lang=lang), "")

        _parse_TODO_find(command=command, lang=lang)

    command.additive["main"] = remove_whitespaces(command.additive["main"])
    return command
