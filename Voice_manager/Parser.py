from Units import Command
from Local import get_base, get_month


def remove_whitespaces(text: str):
    """
    Удаляет из строки лишние пробелы.

    :param text: ``str``: строка, из которой необходимо выделить время.

    :return: Словарь с полями ``hours``, ``minutes``, ``seconds`` в случае,
    если в строке успешно найдены данные времени. В противном случае будет возвращено ``None``.
    """

    cleared = str()
    previous_char = " "

    for char in text:
        if char == " " and previous_char == " ":
            continue

        cleared += char
        previous_char = char

    return cleared


def parse_time(text: str):
    """
    Выделяет из строки время.

    :param text: ``str``: строка, из которой необходимо выделить время.

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
    for i in range(len(units)):
        unit = units[i]

        if unit.isdigit():
            if i + 1 >= len(units):
                break

            next_unit = units[i + 1]
            if next_unit.isdigit():
                return None

            key = get_base(next_unit)
            if key is None:
                return None

            if key == "час":
                if hours_filled:
                    return None

                hours = int(unit)
                hours_filled = True
                continue
            if key == "минута":
                if minutes_filled:
                    return None

                minutes = int(unit)
                minutes_filled = True
                continue
            if key == "секунда":
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


def parse_date(text: str):
    """
    Выделяет из строки дату.

    :param text: ``str``: строка, из которой необходимо выделить дату.

    :return: Словарь с полями ``month``, ``day`` в случае,
        если в строке успешно найдена дата. В противном случае будет возвращено ``None``.
    """

    units = text.split()
    for i in range(len(units)):
        unit = units[i]

        if unit.isdigit():
            if i + 1 >= len(units):
                break

            next_unit = units[i + 1]
            if next_unit.isdigit():
                return None

            base = get_month(next_unit)
            if base is None:
                continue

            day = int(unit)
            month = base

            response = {
                "day": day,
                "month": month
            }

            return response

    return None


def parse_info(command: Command):
    """
    Обрабатывает ``additive`` (дополнительную информацию) переданной команды.

    :param command: ``Command``: обрабатываемая команда.

    :return: Возвращает экземпляр класса ``Command`` - обработанную команду.
    """

    if command.additive["main"] is None:
        return command

    print("[Log: parse]: " + command.additive["main"])

    if command.type == "notification-adding":
        additive = command.additive["main"]
        if additive is None:
            return command

        words = additive.split()

        date = list()
        time = list()
        text = list()

        key = -1
        operational = [
            {
                "keys": ["текст"],
                "source": text
            },
            {
                "keys": ["дата"],
                "source": date
            },
            {
                "keys": ["время"],
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

            if skip:
                continue

            operational[key]["source"].append(word)

        time_response = parse_time(' '.join(time))
        date_response = parse_date(' '.join(date))
        text_response = None if len(text) == 0 else ' '.join(text)

        command.additive["main"] = text_response
        command.additive["time"] = time_response

        if command.key == "add-notification":
            command.additive["date"] = date_response

    if command.key == "delete-notification":
        command.additive["main"] = command.additive["main"].replace("порядковый", "")
        command.additive["main"] = command.additive["main"].replace("номер", "")

    command.additive["main"] = remove_whitespaces(command.additive["main"])
    return command
