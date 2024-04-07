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

        :return:
        """

        self.name = kwargs["name"]
        self.description = kwargs["description"]
        self.function = kwargs["function"]
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

    def __new__(cls, scenarios: list):
        if cls.__instance is None:
            cls.__instance = super(ScenarioInteractor, cls).__new__(cls)
        return cls.__instance

    def __init__(self, scenarios: dict):
        self.scenarios = scenarios

        self.CREATION_SUCCESS_PHRASE = None
        self.DELETION_SUCCESS_PHRASE = None
        self.ALREADY_EXISTS_PHRASE = None
        self.NOT_FOUND_PHRASE = None

    def update_settings(self, __global_context: GlobalContext):
        """
        Метод обновления настроек интерактора сценариев.

        :param __global_context: экземпляр класса глобальных настроек GlobalContext.

        :return:
        """

        self.CREATION_SUCCESS_PHRASE = __global_context.SCENARIO_CREATION_SUCCESS_PHRASE
        self.DELETION_SUCCESS_PHRASE = __global_context.SCENARIO_DELETION_SUCCESS_PHRASE
        self.ALREADY_EXISTS_PHRASE = __global_context.SCENARIO_ALREADY_EXISTS_PHRASE
        self.NOT_FOUND_PHRASE = __global_context.SCENARIO_NOT_FOUND_PHRASE

    def add_scenario(self, **kwargs):
        """
        Метод добавления нового сценария.

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

        :return: Возвращает текст результата выполнения команд сценария.
        """

        name = kwargs["info"]

        if name not in self.scenarios.keys():
            return self.NOT_FOUND_PHRASE

        return self.scenarios[name].execute_scenario()
