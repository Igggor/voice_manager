from context import GlobalContext
from classes import Response
from constants import get_phrase
from meta import SingletonMetaclass


class Scenario:
    """
    Структура сценария.
    """

    def __init__(self, name: str, functions: list):
        """
        Конструктор класса.

        :param name: ``str``: имя (название) сценария;
        :param functions: ``list``: список команд класса ``Command``, которые нужно исполнить при вызове сценария.

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

        output_text = f"Исполняю сценарий { self.name }. \n"
        for item in self.units:
            output_text += item.function(
                **item.static_args,
                info=item.additive
            )

        return Response(
            text=output_text
        )


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

    def update_settings(self):
        """
        Метод обновления настроек интерактора сценариев.

        :return:
        """

        global_context = GlobalContext()

        self.scenarios = global_context.SCENARIOS

    def add_scenario(self, **kwargs):
        """
        Метод добавления нового сценария.

        Обязательные агрументы:
            * ``info``: имя нового сценария;
            * ``subcommands``: команды, которые исполняются при вызове сценария.

        :return: Создает новый сценарий и возвращает фразу-отклик.
        """

        name = kwargs["info"]
        scenario = kwargs["subcommands"]

        if name in self.scenarios.keys():
            # Scenario with this name already exists
            return Response(
                text=get_phrase("SCENARIO_ALREADY_EXISTS_ERROR"),
                is_correct=False
            )

        self.scenarios[name] = Scenario(name, scenario)
        # success
        return Response(
            text=get_phrase("SCENARIO_CREATION_SUCCESS") + name + '.'
        )

    def delete_scenario(self, **kwargs):
        """
        Метод удаления сценария.

        Обязательные агрументы:
            * ``info``: имя удаляемого сценария.

        :return: Пытается удалить сценарий по предоставленному названию и возвращает фразу-отклик.
        """

        name = kwargs["info"]

        if name not in self.scenarios.keys():
            return Response(
                text=get_phrase("SCENARIO_NOT_FOUND_ERROR"),
                is_correct=False
            )

        del self.scenarios[name]
        return Response(
            text=get_phrase("SCENARIO_DELETION_SUCCESS")
        )

    def execute(self, **kwargs):
        """
        Выполнение сценария по заданному в парметрах имени.

        Обязательные агрументы:
            * ``info``: имя исполняемого сценария.

        :return: Возвращает текст результата выполнения команд сценария с заданным именем.
        """

        name = kwargs["info"]

        if name not in self.scenarios.keys():
            return Response(
                text=get_phrase("SCENARIO_NOT_FOUND_ERROR"),
                is_correct=False
            )

        return self.scenarios[name].execute_scenario()
