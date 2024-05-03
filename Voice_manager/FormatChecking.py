from Units import Command, Response
from Metaclasses import SingletonMetaclass

from copy import deepcopy


class FormatChecker(metaclass=SingletonMetaclass):
    """
    ``Singleton``-класс, отвечающий за проверку формата команд.

    **Поля класса:**
        * ``recognition_error`` - ``Response``-объект, возвращаемый при ошибке распознавания команды;
        * ``wrong_command_format_error`` - ``Response``-объект, возвращаемый при нахождении ошибки формата.

    **Методы класса:**
        * ``check_recognition()`` - метод проверки на корректность распознавания;
        * ``check_format()`` - метод проверки формата команды.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(FormatChecker, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.recognition_error = Response(
            text="Команда не распознана",
            error=True
        )

        self.wrong_command_format_error = Response(
            text="Неправильный формат запрашиваемой команды: ",
            error=True
        )

    def check_recognition(self, selected_actions: list):
        """
        Проверка корректности распознавания.

        :param selected_actions: ``list``: проверяемый список команд.

        :return: Обнаруженная ошибка, упакованная в класс Response, или None.
        """

        if len(selected_actions) == 0:
            return self.recognition_error

        return None

    def check_format(self, current_command: Command):
        """
        Проверка формата расшифрованной команды.

        :param current_command: ``Command``: проверяемая команда.

        :return: Обнаруженная ошибка формата, упакованная в ``Response``, или ``None``.
        """

        # Checking forbidden scenario working
        error = deepcopy(self.wrong_command_format_error)
        error.text += f"{current_command.name.lower()}."
        error.called_by = current_command

        # Checking arguments
        if "main" in current_command.required_params and current_command.additive["main"] is None:
            error.info = "Недостаточно параметров к команде."

            return error

        if "subcommands" in current_command.required_params and current_command.additive["subcommands"] is None:
            error.info = "Необходимо указать команды для исполнения."

            return error

        if "time" in current_command.required_params and current_command.additive["time"] is None:
            error.info = "Заданы неправильные параметры к команде: указано некорректное время."

            return error

        if "language" in current_command.required_params and current_command.additive["language"] is None:
            error.info = "Указан неправильный язык."

            return error

        if (current_command.type == "scenario" and
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

        return None
