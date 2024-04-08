from GlobalContext import *


class Command:
    """
    Структура команды (запроса к голосовому помощнику).
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Инициализирует имя команды, её описание, функцию для исполнения, доп. информацию к запросу,
        постоянные агументы, а также подкоманды (специально для сценариев).

        Обязательные агрументы:
            * name: имя команды;
            * function: исполняемая функция;
            * type: тип команды;
            * key: ключ команды
        Опциональные команды:
            * description: описание команды;
            * triggers: ключевые слова для вызова команды;
            * additive_required: обязательна ли доп. информация к команде;
            * subcommands_required: необходимы ли подкоманды.

        :return:
        """

        self.name = kwargs["name"]
        self.description = None if "description" not in kwargs.keys() else kwargs["description"]
        self.key = kwargs["key"]
        self.function = kwargs["function"]
        self.triggers = list() if "triggers" not in kwargs.keys() else kwargs["triggers"]
        self.type = kwargs["type"]

        self.additive_required = False if "additive_required" not in kwargs.keys() else kwargs["additive_required"]
        self.subcommands_required = False if "subcommands_required" not in kwargs.keys() else (
            kwargs["subcommands_required"])

        self.additive = None
        self.static_args = dict()
        self.subcommands = list()

    def update_args(self, **kwargs):
        """
        Обновление статических аргументов команды.

        :return:
        """

        self.static_args = kwargs


class Scenario:
    """
    Структура сценария.
    """

    def __init__(self, name: str, functions: list):
        """
        Конструктор класса.

        :param name: str: имя (название) сценария;
        :param functions: list: список команд класса Command, которые нужно исполнить при вызове сценария.

        Инициализирует название сценария, а также команды, которые исполняются при его вызове.

        :return:
        """

        self.name = name
        self.units = functions

    def execute_scenario(self):
        """
        Выполнение сценария.

        :return: Возвращает текст результата выполнения команд сценария.
        """

        output_text = f"Исполняю сценарий { self.name }. \n\n"
        for item in self.units:
            output_text += item.function(
                **item.static_args,
                info=item.additive
            )

            output_text += "\n"

        return output_text


class ScenarioInteractor:
    """
        Класс, отвечающий за работу со сценариями.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ScenarioInteractor, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.scenarios = None

        self.CREATION_SUCCESS_PHRASE = None
        self.DELETION_SUCCESS_PHRASE = None
        self.ALREADY_EXISTS_PHRASE = None
        self.NOT_FOUND_PHRASE = None

    def update_settings(self):
        """
        Метод обновления настроек интерактора сценариев.

        :return:
        """

        global_context = GlobalContext()

        self.scenarios = global_context.scenarios

        self.CREATION_SUCCESS_PHRASE = global_context.SCENARIO_CREATION_SUCCESS_PHRASE
        self.DELETION_SUCCESS_PHRASE = global_context.SCENARIO_DELETION_SUCCESS_PHRASE
        self.ALREADY_EXISTS_PHRASE = global_context.SCENARIO_ALREADY_EXISTS_PHRASE
        self.NOT_FOUND_PHRASE = global_context.SCENARIO_NOT_FOUND_PHRASE

    def add_scenario(self, **kwargs):
        """
        Метод добавления нового сценария.

        Обязательные агрументы:
            * info: имя нового сценария;
            * subcommands: команды, которые исполняются при вызове сценария.

        :return: Создает новый сценарий и возвращает фразу-отклик.
        """

        name = kwargs["info"]
        scenario = kwargs["subcommands"]

        if name in self.scenarios.keys():
            # Scenario with this name already exists
            return self.ALREADY_EXISTS_PHRASE

        self.scenarios[name] = Scenario(name, scenario)
        # success
        return self.CREATION_SUCCESS_PHRASE + name

    def delete_scenario(self, **kwargs):
        """
        Метод удаления сценария.

        Обязательные агрументы:
            * info: имя удаляемого сценария.

        :return: Пытается удалить сценарий по предоставленному названию и возвращает фразу-отклик.
        """

        name = kwargs["info"]

        if name not in self.scenarios.keys():
            return self.NOT_FOUND_PHRASE

        del self.scenarios[name]
        return self.DELETION_SUCCESS_PHRASE

    def execute(self, **kwargs):
        """
        Выполнение сценария по заданному в парметрах имени.

        Обязательные агрументы:
            * info: имя исполняемого сценария.

        :return: Возвращает текст результата выполнения команд сценария.
        """

        name = kwargs["info"]

        if name not in self.scenarios.keys():
            return self.NOT_FOUND_PHRASE

        return self.scenarios[name].execute_scenario()
