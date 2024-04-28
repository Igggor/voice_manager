from GlobalContext import GlobalContext
from Units import Scenario
from Metaclasses import SingletonMetaclass


class ScenarioInteractor(metaclass=SingletonMetaclass):
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

        self.scenario_already_exists_error = None
        self.scenario_creation_success = None
        self.scenario_deletion_success = None
        self.scenario_not_found_error = None

    def update_settings(self):
        """
        Метод обновления настроек интерактора сценариев.

        :return:
        """

        global_context = GlobalContext()

        self.scenarios = global_context.SCENARIOS

        self.scenario_already_exists_error = global_context.scenario_already_exists_error
        self.scenario_creation_success = global_context.scenario_creation_success
        self.scenario_deletion_success = global_context.scenario_deletion_success
        self.scenario_not_found_error = global_context.scenario_not_found_error

    def add_scenario(self, **kwargs):
        """
        Метод добавления нового сценария.

        Обязательные агрументы:
            * ``info``: имя нового сценария;
            * ``subcommands``: команды, которые исполняются при вызове сценария.

        :return: Создает новый сценарий и возвращает фразу-отклик.
        """

        name = kwargs["main"]
        scenario = kwargs["subcommands"]

        if name in self.scenarios.keys():
            # Scenario with this name already exists
            return self.scenario_already_exists_error

        self.scenarios[name] = Scenario(name, scenario)
        # success
        response = self.scenario_creation_success
        response.info = f"{name}."
        return response

    def delete_scenario(self, **kwargs):
        """
        Метод удаления сценария.

        Обязательные агрументы:
            * ``info``: имя удаляемого сценария.

        :return: Пытается удалить сценарий по предоставленному названию и возвращает фразу-отклик.
        """

        name = kwargs["main"]

        if name not in self.scenarios.keys():
            return self.scenario_not_found_error

        del self.scenarios[name]
        return self.scenario_deletion_success

    def execute(self, **kwargs):
        """
        Выполнение сценария по заданному в парметрах имени.

        Обязательные агрументы:
            * ``info``: имя исполняемого сценария.

        :return: Возвращает текст результата выполнения команд сценария с заданным именем.
        """

        name = kwargs["main"]

        if name not in self.scenarios.keys():
            return self.scenario_not_found_error

        return self.scenarios[name].execute_scenario()
