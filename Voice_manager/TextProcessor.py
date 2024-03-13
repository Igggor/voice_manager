class TextProcessor:
    """
    Класс, отвечающий за сопоставление текста с необходимой командой.
    Singleton - pattern
    """
    __instance = None

    def __new__(cls, name: str):
        if cls.__instance is None:
            cls.__instance = super(TextProcessor, cls).__new__(cls)
        return cls.__instance

    def __init__(self, name: str):
        """
        Конструктор класса.
        Инициалиация словаря доступных команд AVAILABLE_COMMANDS, фразы приветствия (при включении) и прощания
        (при выключении).

        :param name:
        """
        self.AVAILABLE_COMMANDS = {
            "alias": name,
            "tbr": ("помоги", "скажи", "расскажи", "покажи", "сколько", "произнеси", "какой"),
            "commands": {
                "here": ["тут", "спишь", "на месте"],
                "thanks": ["спасибо", "благодарю", "благодарствую"],
                "off": ["пока", "отключись", "до свидания"],
                "on": ["привет", "приветствую", "приветик", "ку", "здравия"],
                "time": ["текущее время", "времени", "который час"],
                "weather": ["какая погода", "погода", "погоду"],
                "course": ["евро", "доллар", "курс валют"],
                "features": ['что умеешь']
            }
        }

        self.GREETING_PHRASE = (f"Приветствую, я твой универсальный помощник { name }. Ты можешь узнать о "
                                f"моих возможностях на сайте или просто спросив меня: { name }, что ты умеешь?")

        self.BYE_PHRASE = "Всего доброго, была рада помочь."
        self.RECOGNITION_ERROR_PHRASE = "Команда не распознана."

    def clean(self, command: str):
        """
        Очистка текста, выделяющая из него только необходимые для распознавания команды части.

        :param command: строка с распознанным текстом.

        :return: строка с командой
        """
        for item in self.AVAILABLE_COMMANDS['alias']:
            command = command.replace(item, "").strip()
        for item in self.AVAILABLE_COMMANDS['tbr']:
            command = command.replace(item, "").strip()

        return command

    # Важно! В текущем варианте строку можно сопоставить только одной команде. Иначе говоря, одной фразе соответствует
    # ОДНА произвольная команда из этой фразы (та, которая будет найдена первой).
    # *Комментарий автора: будет невероятно удобно, если так и останется)

    # В РАЗРАБОТКЕ.

    # Важно! В этом методе планируется реализовать запись логов
    # (примерный вид: запрос -> что подошло -> доп. информация).
    def match_command(self, command: str, ignore_all: bool):
        """
        Поиск команды в словаре AVAILABLE_COMMANDS

        :param command: строка с командой;
        :param ignore_all: Булевая метка. Если ignore_all = True, то учитывается только команда ON.

        :return: Если в тексте не найдено обращения к голосовому помощнику, будет возвращено None.
                 Если обращение к голосовому помощнику найдено, однако в AVAILABLE_COMMANDS не существует запрашиваемой
                 команды, будет возвращён служебный ключ "N-F". В случае успешного распознавания команды будет возвращен
                 ключ этой команды.
        """
        if not command.startswith(self.AVAILABLE_COMMANDS["alias"]):
            return None

        command = self.clean(command)
        if ignore_all:
            if command in self.AVAILABLE_COMMANDS["commands"]["on"]:
                return "on"

            return None

        for key, values in self.AVAILABLE_COMMANDS["commands"]:
            if command in values:
                return key

        return "N-F"
