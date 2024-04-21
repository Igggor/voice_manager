from GlobalContext import GlobalContext
from Classes import Response


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

        self.scenarios = global_context.SCENARIOS

        self.CREATION_SUCCESS_PHRASE = global_context.SCENARIO_CREATION_SUCCESS_PHRASE
        self.DELETION_SUCCESS_PHRASE = global_context.SCENARIO_DELETION_SUCCESS_PHRASE
        self.ALREADY_EXISTS_PHRASE = global_context.SCENARIO_ALREADY_EXISTS_PHRASE
        self.NOT_FOUND_PHRASE = global_context.SCENARIO_NOT_FOUND_PHRASE

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
                text=self.ALREADY_EXISTS_PHRASE,
                is_correct=False
            )

        self.scenarios[name] = Scenario(name, scenario)
        # success
        return Response(
            text=self.CREATION_SUCCESS_PHRASE + name + '.'
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
                text=self.NOT_FOUND_PHRASE,
                is_correct=False
            )

        del self.scenarios[name]
        return Response(
            text=self.DELETION_SUCCESS_PHRASE
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
                text=self.NOT_FOUND_PHRASE,
                is_correct=False
            )

        return self.scenarios[name].execute_scenario()
