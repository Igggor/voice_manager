from GlobalContext import GlobalContext


class TextProcessor:
    """
    Класс, отвечающий за сопоставление текста с необходимой командой.
    Singleton - pattern
    """
    __instance = None

    def __new__(cls, __global_context: GlobalContext):
        if cls.__instance is None:
            cls.__instance = super(TextProcessor, cls).__new__(cls)
        return cls.__instance

    def __init__(self, __global_context: GlobalContext):
        """
        Конструктор класса.
        Инициалиация словаря доступных команд AVAILABLE_COMMANDS, фразы приветствия (при включении) и прощания
        (при выключении).

        :param __global_context: глобальные настройки.
        """

        # AVAILABLE_COMMANDS должен быть переработан (наверное)
        self.AVAILABLE_COMMANDS = {
            "alias": "Name",
            "commands": {
                "thanks": ["спасибо", "благодарю"],
                "off": ["отключись"],
                "on": ["привет", "включись"],
                "time": ["текущее время", "сколько времени"],
                "weather-now": ["какая сейчас погода", "текущая погода"],
                "course": ["курс валют"],
                "features": ["что ты умеешь"]
            }
        }

        self.update_settings(__global_context)

    def update_settings(self, __global_context: GlobalContext):
        """
        Метод обновления настроек текстового процессора.

        :param __global_context: экземпляр класса глобальных настроек GlobalContext
        """

        self.AVAILABLE_COMMANDS["alias"] = __global_context.NAME

    # В РАЗРАБОТКЕ.
    def clean(self, command: str, pick_additive: bool = False):
        """
        Очистка текста, выделяющая из него только необходимые для распознавания команды части.

        :param command: str: строка с распознанным текстом.
        :param pick_additive: bool: если задано True, то в запросе выделяется только доп. информация.

        :return: Строка с полученной командой.
        """
        for item in self.AVAILABLE_COMMANDS['alias']:
            command = command.replace(item, "").strip()

        if pick_additive:
            for item in self.AVAILABLE_COMMANDS['commands']:
                command = command.replace(item, "").strip()

        return None if command == "" else command

    # Важно! В текущем варианте строку можно сопоставить только одной команде. Иначе говоря, одной фразе соответствует
    # ОДНА произвольная команда из этой фразы (та, которая будет найдена первой).
    # *Комментарий автора: будет невероятно удобно, если так и останется)

    # Важно! В этом методе планируется реализовать запись логов
    # (примерный вид: запрос -> что подошло -> доп. информация).
    # В РАЗРАБОТКЕ.
    def match_command(self, command: str, ignore_all: bool):
        """
        Поиск команды в словаре AVAILABLE_COMMANDS
        Возвращает пару вида {ключ команды; дополнительные данные}.

        :param command: строка с командой;
        :param ignore_all: bool-метка. Если ignore_all = True, то учитывается только команда ON.

        :return: Если в тексте не найдено обращения к голосовому помощнику, будет возвращено { None; None }.
                 Если обращение к голосовому помощнику найдено, однако в AVAILABLE_COMMANDS не существует запрашиваемой
                 команды, будет возвращён служебный ключ { "С-N-F", None }. В случае успешного распознавания команды
                 будет возвращен ключ этой команды и, возможно, доп. параметры или None в зависимости от типа команды.
        """
        if not command.startswith(self.AVAILABLE_COMMANDS["alias"]):
            return None, None

        command = self.clean(command)
        if ignore_all:
            if command in self.AVAILABLE_COMMANDS["commands"]["on"]:
                return "on", None

            return None, None

        for key, values in self.AVAILABLE_COMMANDS["commands"]:
            if command in values:
                return key, self.clean(command, True)

        return "С-N-F", None
