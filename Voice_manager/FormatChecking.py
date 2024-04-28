from Units import Command
from Metaclasses import SingletonMetaclass
from GlobalContext import GlobalContext


class FormatChecker(metaclass=SingletonMetaclass):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(FormatChecker, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.recognition_error = None
        self.wrong_command_format_error = None

    def update_settings(self):
        global_context = GlobalContext()

        self.recognition_error = global_context.recognition_error
        self.wrong_command_format_error = global_context.wrong_command_format_error

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
        error = self.wrong_command_format_error
        error.info = f"{current_command.name.lower()}. \n"
        error.called_by = current_command

        # Checking arguments
        if current_command.additive_required and current_command.additive["main"] is None:
            error.info += "Недостаточно параметров к команде."

            return error

        if current_command.subcommands_required and ("subcommands" not in current_command.additive.keys() or
                                                     len(current_command.additive["subcommands"])) == 0:
            error.info += "Необходимо указать команды для исполнения."

            return error

        if (current_command.type == "scenario" and
                any(sub.type == "scenario" for sub in current_command.additive["subcommands"])):
            error.info += "Внутри сценария нельзя работать с другими сценариями."

            return error

        if current_command.type == "notification-adding":
            hours, minutes, seconds = current_command.additive["time"].values()
            if current_command.key == "add-notification" and (hours < 0 or hours > 23):
                error.info += ("Заданы неправильные параметры к команде: количество часов должно быть в пределах "
                               "от 0 до 23.")

                return error

            if minutes < 0 or minutes > 59:
                error.info += ("Заданы неправильные параметры к команде: количество минут должно быть в пределах "
                               "от 0 до 59.")

                return error

            if seconds < 0 or seconds > 59:
                error.info += ("Заданы неправильные параметры к команде: количество секунд должно быть в пределах "
                               "от 0 до 59.")

                return error

            if hours == 0 and minutes == 0 and seconds < 10 and current_command.key == "add-timer":
                error.info += "Не рекомендуется устанавливать таймер на время менее 10 секунд."

                return error

        return None
