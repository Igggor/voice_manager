from Units import Command
from Local import get_base, get_month


def parse_time(text: str):
    hours = 0
    minutes = 0
    seconds = 0

    hours_filled = False
    minutes_filled = False
    seconds_filled = False

    units = text.split()
    for i in range(len(units)):
        unit = units[i]
        if ':' in unit:
            if hours_filled or minutes_filled:
                return None

            hours, minutes = map(int, unit.split(':'))

            hours_filled = True
            minutes_filled = True
            continue

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

    response = {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }

    print('[Log: time_parse]: ', response)
    return response


def parse_date(text: str):
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
        text_response = ' '.join(text)

        command.additive["main"] = text_response
        command.additive["time"] = time_response

        if command.key == "add-notification":
            command.additive["date"] = date_response

    return command
