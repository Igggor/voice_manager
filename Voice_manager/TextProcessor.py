from GlobalContext import GlobalContext
from Functions import FunctionsCore
from Classes import Command
from Scenarios import ScenarioInteractor


class TextProcessor:
    """
    Класс, отвечающий за сопоставление текста с необходимой командой.
    """

    __instance = None

    def __new__(cls, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(TextProcessor, cls).__new__(cls)
        return cls.__instance

    def __init__(self, **kwargs):
        """
        Конструктор класса.
        Инициалиация словаря доступных команд, фразы приветствия (при включении) и прощания (при выключении).

        Обязательные параметры: системные функции из головного класса VoiceHelper.

        :return:
        """

        set_ON = kwargs["set_ON"]
        features = kwargs["features"]
        thanks = kwargs["thanks"]
        set_OFF = kwargs["set_OFF"]
        safe_exit = kwargs["exit"]

        scenario_interactor = ScenarioInteractor()
        functions_core = FunctionsCore()

        self.NAME = None

        # В РАЗРАБОТКЕ, все функции помощника должны быть здесь.
        # Каждая функция возвращает структуру Response.
        self.functions = {
            "on":
                Command(
                    name="Включение голосового помощника.",
                    description="Во включенном состоянии глосовой помощник прослушивает команды и исполняет их.",
                    key="on",
                    function=set_ON,
                    triggers=["привет", "включись", "включение"],
                    type="system"
                ),
            "features":
                Command(
                    name="Возможности голосового помощника.",
                    key="features",
                    function=features,
                    triggers=["что ты умеешь", "возможности"],
                    type="question"
                ),
            "thanks":
                Command(
                    name="Рада стараться.",
                    key="thanks",
                    function=thanks,
                    triggers=["спасибо", "благодарю"],
                    type="question"
                ),
            "full-off":
                Command(
                    name="Полное выключение голосового помощника",
                    description="Выключение приложения",
                    key="full-off",
                    function=safe_exit,
                    triggers=["отключись полностью", "отключить полностью", "полное отключение"],
                    type="system"
                ),
            "off":
                Command(
                    name="Перевод голосового помощника в режим гибернации",
                    description="В режиме сна приложение не закрывается, однако не воспринимает голосовые команды",
                    key="off",
                    function=set_OFF,
                    triggers=["отключись", "отключение"],
                    type="system"
                ),
            "time":
                Command(
                    name="Получение текущего времени",
                    description="Голосовой помощник получает системное время и озвучивает его",
                    key="time",
                    function=functions_core.get_time_now,
                    triggers=["сколько времени", "текущее время"],
                    type="question"
                ),
            "date":
                Command(
                    name="Получение текущей даты",
                    description="Голосовой помощник получает текущую дату и озвучивает её",
                    key="date",
                    function=functions_core.get_date,
                    triggers=["какой сегодня день", "сегодняшняя дата", "текущая дата"],
                    type="question"
                ),
            "course":
                Command(
                    name="Получение текущего курса валют",
                    description="Голосовой помощник получает курс доллара и евро к рублю Центрального Банка России "
                                "(по состоянию на данный момент) и озвучивает его",
                    key="course",
                    function=functions_core.get_currency_course,
                    triggers=["курс валют"],
                    type="question"
                ),
            "weather-now":
                Command(
                    name="Получение текущей погоды",
                    description="Голосовой помощник получает текущую погоду с заданными параметрами и озвучивает её",
                    key="weather-now",
                    function=functions_core.get_weather_now,
                    triggers=["какая сейчас погода", "текущая погода", "погода"],
                    type="question"
                ),
            "create-scenario":
                Command(
                    name="Создание сценария",
                    description="Создание группы команд с заданным именем, выполняющихся поочередно",
                    key="create-scenario",
                    function=scenario_interactor.add_scenario,
                    triggers=["создай сценарий", "добавь сценарий", "добавление сценария"],
                    type="scenario",
                    additive_required=True,
                    subcommands_required=True
                ),
            "execute-scenario":
                Command(
                    name="Исполнение сценария",
                    description="Исполнение заданной группы команд, "
                                "в том порядке, в котором они были даны при создании",
                    key="execute-scenario",
                    function=scenario_interactor.execute,
                    triggers=["запусти сценарий", "исполни сценарий", "исполнение сценария"],
                    type="scenario",
                    additive_required=True
                ),
            "delete-scenario":
                Command(
                    name="Удаление сценария",
                    description="Удаление группы команд по заданному имени",
                    key="delete-scenario",
                    function=scenario_interactor.delete_scenario,
                    triggers=["удали сценарий", "удаление сценария"],
                    type="scenario",
                    additive_required=True
                )
        }

    def update_settings(self):
        """
        Метод обновления настроек текстового процессора.

        :return:
        """

        global_context = GlobalContext()
        self.NAME = [global_context.NAME.lower()]

    # В РАЗРАБОТКЕ.
    def clean_alias(self, command: str):
        """
        Метод, удаляющий обращение к помощнику.

        :param command: str: строка с распознанным текстом.

        :return: Строка с полученной командой.
        """

        for item in self.NAME:
            command = command.replace(item, "").strip()

        return None if command == "" else command

    def clean_extend(self, command: str, prefix: str):
        """
        Выделение доп. информации для конкретной команды, заданной параметром prefix.

        :param command: str: строка с распознанным текстом;
        :param prefix: str: текст команды, для которой необходимо найти доп. информацию.

        :return: Доп. информация к этой команде / None, если таковой нет.
        """

        command = command[len(prefix) + 1:]

        for key, value in self.functions.items():
            for v in value.triggers:
                find_result = command.find(v)
                if find_result == -1:
                    continue

                # если find_result == 0, то пробела, который нужно удалить, перед ним нет, и вычитать единицу не нужно.
                command = command[:(0 if find_result == 0 else find_result - 1)]

        return None if command == "" else command

    def pick_additive(self, command: str, index: int):
        """
        Выделение доп. информации для команды, заданной положением в строке.

        :param command: str: строка с распознанным текстом;
        :param index: int: индекс в строке (нумерация с нуля), с которого, предположительно, начинается команда,
                           для которой нужно выделить доп. информацию.

        :return: Если найдена команда, начинающаяся со слова с индексом index, то будет возвращена
        искомая команда с дополнительной информацией.
        """

        command = ' '.join(command.split()[index:])
        for key, value in self.functions.items():
            for v in value.triggers:
                if not command.startswith(v):
                    continue

                additive_info = self.clean_extend(command, v)
                out = self.functions[key]
                out.additive = additive_info
                return out

        return None

    # В РАЗРАБОТКЕ.
    def match_command(self, command: str, ignore_all: bool):
        """
        Поиск команды среди доступных.
        Возвращает список распознанных команд.

        :param command: str: строка с командой;
        :param ignore_all: bool: если ``ignore_all`` = True, то учитывается только команда ON.

        :return: Если в тексте не найдено обращения к голосовому помощнику, будет возвращёно None.
                 Если обращение к голосовому помощнику найдено, однако не существует запрашиваемой
                 команды, будет возвращен пустой список.
                 Иначе будет возвращен список из распознанных команд.
        """

        selected_actions = list()
        if not any(command.startswith(alias) for alias in self.NAME):
            return None

        command = self.clean_alias(command)
        if ignore_all:
            if any(on in command for on in self.functions["on"].triggers):
                selected_actions.append(self.functions["on"])
            else:
                return None

            return selected_actions

        command_size = len(command.split())
        for it in range(command_size):
            picking_result = self.pick_additive(command, it)
            if picking_result is None:
                continue

            selected_actions.append(picking_result)

        for i in range(len(selected_actions)):
            current_command = selected_actions[i]
            if current_command.key == "create-scenario":
                current_command.subcommands = selected_actions[(i + 1):]

                del selected_actions[(i + 1):]
                break

        return selected_actions
