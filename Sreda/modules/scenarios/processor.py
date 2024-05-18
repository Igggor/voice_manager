from Sreda.settings import GlobalContext

from Sreda.modules.scenarios.units import Scenario
from Sreda.modules.text.units import Response

from Sreda.static.metaclasses import SingletonMetaclass

from copy import deepcopy


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
        self.scenarios_limit = None

        self.scenario_already_exists_error = None
        self.scenario_creation_success = None

        self.scenario_deletion_success = Response(
            text="Сценарий успешно удалён."
        )

        self.scenario_not_found_error = Response(
            text=("Запрошенный сценарий не найден. \n"
                  "Уточните команду и повторите попытку."),
            error=True
        )
        self.scenarios_overflow_error = None

    def update_settings(self) -> None:
        """
        Метод обновления настроек интерактора сценариев.

        :return:
        """

        global_context = GlobalContext()

        self.scenarios = global_context.SCENARIOS
        self.scenarios_limit = global_context.scenarios_limit

        self.scenario_creation_success = Response(
            text=(f"Сценарий успешно создан. \n"
                  f"Вы можете запустить его, сказав: {global_context.NAME}, запусти сценарий "),
        )

        self.scenario_already_exists_error = Response(
            text=(f"Сценарий с данным именем уже существует. \n"
                  f"Попробуйте изменить имя создаваемого сценария. \n"
                  f"Также Вы можете удалить старый сценарий, сказав: {global_context.NAME}, удали сценарий."),
            error=True
        )
        self.scenarios_overflow_error = Response(
            text=f"Достигнут лимит количества сценариев. "
                 f"Вы можете увеличить его в настройках или удалить произвольный сценарий, сказав: "
                 f"{global_context.NAME}, удали сценарий. Не забудьте указать имя удаляемого сценария.",
            error=True
        )

        self._shrink()

    def _shrink(self) -> None:
        """
        Удаляет старые сценарии до того момента, пока количество сценариев превышает лимит.

        :return:
        """

        while len(self.scenarios) > self.scenarios_limit:
            del self.scenarios[0]

    def add_scenario(self, **kwargs) -> Response:
        """
        Метод добавления нового сценария.

        Обязательные агрументы:
            * ``info``: имя нового сценария;
            * ``subcommands``: команды, которые исполняются при вызове сценария.

        :return: Создает новый сценарий и возвращает фразу-отклик.
        """

        name = kwargs["main"]
        scenario = kwargs["subcommands"]

        if len(self.scenarios) + 1 > self.scenarios_limit:
            return self.scenarios_overflow_error

        if name in self.scenarios.keys():
            # Scenario with this name already exists
            return self.scenario_already_exists_error

        self.scenarios[name] = Scenario(name=name, functions=scenario)

        # success
        response = deepcopy(self.scenario_creation_success)
        response.text += f"{name}."

        return response

    def delete_scenario(self, **kwargs) -> Response:
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

    def execute(self, **kwargs) -> Response:
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
