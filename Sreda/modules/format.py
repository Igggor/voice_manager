from Sreda.modules.text.units import Command, Response

from Sreda.static.constants import FULL_SUPPORTED_LANGUAGES

import datetime


def check_recognition(selected_actions: list[Command]) -> Response | None:
    """
    Проверка корректности распознавания.

    :param selected_actions: ``list``: проверяемый список команд.

    :return: Обнаруженная ошибка, упакованная в класс Response, или None.
    """

    if len(selected_actions) == 0:
        return Response(
            text="Команда не распознана",
            error=True
        )

    return None


def check_format(current_command: Command) -> Response | None:
    """
    Проверка формата расшифрованной команды.

    :param current_command: ``Command``: проверяемая команда.

    :return: Обнаруженная ошибка формата, упакованная в ``Response``, или ``None``.
    """

    # Checking forbidden scenario working
    error = Response(
        text=f"Неправильный формат запрашиваемой команды: {current_command.name.lower()}.",
        called_by=current_command,
        error=True
    )

    # Checking arguments
    if "main" in current_command.required_params and ("main" not in current_command.additive.keys() or
                                                      current_command.additive["main"] is None):
        error.info = "Недостаточно параметров к команде."

        return error

    if "subcommands" in current_command.required_params and ("subcommands" not in current_command.additive.keys() or
                                                             current_command.additive["subcommands"] is None):
        error.info = "Необходимо указать команды для исполнения."

        return error

    if "time" in current_command.required_params and ("time" not in current_command.additive.keys() or
                                                      current_command.additive["time"] is None):
        error.info = "Заданы неправильные параметры к команде: указано некорректное время."

        return error

    if "date" in current_command.required_params and ("date" not in current_command.additive.keys() or
                                                      current_command.additive["date"] is None):
        error.info = "Заданы неправильные параметры к команде: указана некорректная дата."

        return error

    if "language" in current_command.required_params and ("language" not in current_command.additive.keys() or
                                                          current_command.additive["language"] is None):
        error.info = "Указан неправильный язык."

        return error

    if (current_command.key == "create-scenario" and
            any(sub.type == "scenario" for sub in current_command.additive["subcommands"])):
        error.info = "Внутри сценария нельзя работать с другими сценариями."

        return error

    if current_command.type == "notification-adding":
        hours, minutes, seconds = current_command.additive["time"].values()
        if current_command.key == "add-notification" and (hours < 0 or hours > 23):
            error.info = ("Заданы неправильные параметры к команде: количество часов должно быть в пределах "
                          "от 0 до 23.")

            return error

        if minutes < 0 or minutes > 59:
            error.info = ("Заданы неправильные параметры к команде: количество минут должно быть в пределах "
                          "от 0 до 59.")

            return error

        if seconds < 0 or seconds > 59:
            error.info = ("Заданы неправильные параметры к команде: количество секунд должно быть в пределах "
                          "от 0 до 59.")

            return error

        if hours == 0 and minutes == 0 and seconds < 10 and current_command.key == "add-timer":
            error.info = "Не рекомендуется устанавливать таймер на время менее 10 секунд."

            return error

    if current_command.key == "set-volume":
        new_volume = current_command.additive["main"]
        if not new_volume.isdigit() or int(new_volume < 0) or int(new_volume > 100):
            error.info = ("Заданы неправильные параметры к команде: новое значение громкости звука "
                          "должно быть целым числом от 0 до 100.")

            return error

    if current_command.key == "delete-notification":
        if not current_command.additive["main"].isdigit():
            error.info = "Порядковый номер удаляемого напоминания должен быть целым числом."

            return error

    if "date" in current_command.additive.keys() and current_command.additive["date"] is not None \
            and "today" in current_command.additive["date"].keys() and "time" in current_command.additive.keys():
        hours, minutes, seconds = current_command.additive["time"].values()

        moment = datetime.datetime.now()
        checking = datetime.datetime(
            year=moment.year, month=moment.month, day=moment.day, hour=hours, minute=minutes, second=seconds
        )

        if checking < moment:
            error.info = "Задано некорректное время, указывающее на прошлое."

            return error

    return None


def command_available(current_command: Command, language: str) -> Response | None:
    """
    Проверка на то, что команда доступна на данном языке.

    :param current_command: ``Command``: проверяемая команда;
    :param language: ``str``: код языка.

    :return: Обнаруженная ошибка, упакованная в ``Response``, или ``None``.
    """

    error = Response(
        text="Похоже, эта команда не поддерживается на заданном языке распознавания. Приношу свои извинения.",
        called_by=current_command,
        error=True
    )

    if current_command.numeric_required and language not in FULL_SUPPORTED_LANGUAGES:
        return error

    return None