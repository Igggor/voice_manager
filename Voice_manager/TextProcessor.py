# Класс, отвечающий за сопоставление текста с необходимой командой.
# Singleton - pattern
class TextProcessor:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(TextProcessor, cls).__new__(cls)
        return cls.__instance

    # Конструктор.
    # Инициализирует словарь доступных команд AVAILABLE_COMMANDS, фразы приветствия (при включении)
    # и прощания (при выключении).
    def __init__(self):
        self.AVAILABLE_COMMANDS = {
            "alias": ("помощник", "бот", "помощь", "ты", "среда", "голосовой", "троечка"),
            "tbr": ("помоги", "скажи", "расскажи", "покажи", "сколько", "произнеси", "какой"),
            "commands": {
                "here": ["тут", "спишь", "на месте"],
                "thanks": ["спасибо", "благодарю", "благодарствую"],
                "off": ["пока", "отключись", "до свидания"],
                "on": ["привет", "приветствую", "приветик", "ку", "здравия"],
                "time": ["текущее время", "времени", "который час"],
                "weather": ["какая погода", "погода", "погоду"],
                "course": ["евро", "доллар", "курс валют"],
            }
        }

        self.GREETING_PHRASE = ("Приветствую, я твой универсальный помощник Среда. "
                                "Ты можешь узнать о моих возможностях на сайте или просто спросив меня.")

        self.BYE_PHRASE = "Всего доброго, была рада помочь."

    # Метод.
    # Принимает на вход строку command и убирает из неё обращения к боту, оставляя только непосредственно команду.
    # Возвращает измененную строку.
    def clean(self, command: str):
        for item in self.AVAILABLE_COMMANDS['alias']:
            command = command.replace(item, "").strip()
        for item in self.AVAILABLE_COMMANDS['tbr']:
            command = command.replace(item, "").strip()

        return command

    # Метод.
    # Принимает на вход строку command и пытается сопоставить её с командой, присутствующей в словаре
    # AVAILABLE_COMMANDS. Возвращает строку, соответствующую ключу в словаре AVAILABLE_COMMANDS, если команда
    # была успешно найдена, или None в противном случае.

    # В РАЗРАБОТКЕ.

    # Внимание! В этом методе планируется реализовать запись логов
    # (примерный вид: запрос -> что подошло -> доп. информация).
    def matchCommand(self, command: str):
        if not command.startswith(self.AVAILABLE_COMMANDS["alias"]):
            return

        currentCommands = self.clean(command).split()

        listCommands = list()
        for key, values in self.AVAILABLE_COMMANDS['commands'].items():
            for item in values:
                for comma in currentCommands:
                    if item == comma:
                        listCommands.append(key)

        if len(listCommands):
            return listCommands

        return None
