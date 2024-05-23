from Sreda.settings import GlobalContext

from Sreda.modules.api.processor import APIProcessor
from Sreda.modules.functions.processor import FunctionsCore
from Sreda.modules.time.processor import TimeWorker
from Sreda.modules.text.units import Command
from Sreda.modules.scenarios.processor import ScenarioInteractor
from Sreda.modules.parser.processor import parse_info, canonize_text
from Sreda.modules.speech.processor import SpeechTranslator
from Sreda.modules.translation.processor import Translator
from Sreda.modules.collecting.processor import load_all_triggers, ready_all, ready_all_words
from Sreda.modules.collecting.units import Storage
from Sreda.modules.calendar.processor import TODOInteractor

from Sreda.static.metaclasses import SingletonMetaclass
from Sreda.static.constants import AUXILIARY_WORDS


class TextProcessor(metaclass=SingletonMetaclass):
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

        Обязательные параметры: системные функции из головного класса ``VoiceHelper``.

        :return:
        """

        set_ON = kwargs["set_ON"]
        features = kwargs["features"]
        thanks = kwargs["thanks"]
        set_OFF = kwargs["set_OFF"]
        safe_exit = kwargs["exit"]
        update_all = kwargs["update_settings"]

        scenario_interactor = ScenarioInteractor()
        time_core = TimeWorker()
        functions_core = FunctionsCore()
        speech_translator = SpeechTranslator()
        translator = Translator()
        TODO_interactor = TODOInteractor()
        api_actions = APIProcessor()

        self.language_listen = None

        # В РАЗРАБОТКЕ, все функции помощника должны быть здесь.
        # Каждая функция возвращает структуру Response.
        self.functions = {
            "notification":
                Command(
                    name=None, description=None, key="notification", function=None, type="system-call"
                ),

            "on":
                Command(
                    name="Включение голосового помощника",
                    description="Во включенном состоянии глосовой помощник прослушивает команды и исполняет их",
                    key="on", function=set_ON, type="system"
                ),
            "update-settings":
                Command(
                    name="Обновление настроек помощника",
                    description="Настройки будут синхронизированы с web-приложением", key="update-settings",
                    function=update_all, type="system"
                ),
            "features":
                Command(
                    name="Возможности голосового помощника",
                    key="features", function=features, type="question"
                ),
            "thanks":
                Command(
                    name="Рада стараться",
                    key="thanks", function=thanks, type="question"
                ),
            "full-off":
                Command(
                    name="Полное выключение голосового помощника",
                    description="Выключение приложения",
                    key="full-off", function=safe_exit, type="system"
                ),
            "off":
                Command(
                    name="Перевод голосового помощника в режим гибернации",
                    description="В режиме сна приложение не закрывается, однако не воспринимает голосовые команды",
                    key="off", function=set_OFF, type="system"
                ),
            "time":
                Command(
                    name="Получение текущего времени",
                    description="Голосовой помощник получает системное время и озвучивает его",
                    key="time", function=time_core.get_time_now, type="question"
                ),
            "date":
                Command(
                    name="Получение текущей даты",
                    description="Голосовой помощник получает текущую дату и озвучивает её",
                    key="date", function=time_core.get_date, type="question"
                ),
            "course":
                Command(
                    name="Получение текущего курса валют",
                    description="Голосовой помощник получает курс доллара и евро к рублю Центрального Банка России "
                                "(по состоянию на данный момент) и озвучивает его",
                    key="course", function=functions_core.get_currency_course, type="question"
                ),
            "weather-now":
                Command(
                    name="Получение текущей погоды",
                    description="Голосовой помощник получает текущую погоду с заданными параметрами и озвучивает её",
                    key="weather-now", function=functions_core.get_weather_now, type="question"
                ),
            "create-scenario":
                Command(
                    name="Создание сценария",
                    description="Создание группы команд с заданным именем, выполняющихся поочередно",
                    key="create-scenario", function=scenario_interactor.add_scenario, type="scenario",
                    required_params=["main", "subcommands"]
                ),
            "execute-scenario":
                Command(
                    name="Исполнение сценария",
                    description="Исполнение заданной группы команд, "
                                "в том порядке, в котором они были даны при создании",
                    key="execute-scenario", function=scenario_interactor.execute, type="scenario",
                    required_params=["main"]
                ),
            "delete-scenario":
                Command(
                    name="Удаление сценария",
                    description="Удаление группы команд по заданному имени",
                    key="delete-scenario", function=scenario_interactor.delete_scenario, type="scenario",
                    required_params=["main"]
                ),
            "add-notification":
                Command(
                    name="Добавление напоминания",
                    description="Добавление напоминания с заданным текстом и временем запуска",
                    key="add-notification", function=time_core.notifications_interactor.add_notification,
                    type="notification-adding", required_params=["time"], ignore_following=True, numeric_required=True
                ),
            "add-timer":
                Command(
                    name="Добавление таймера",
                    description="Добавление таймера на заданное количество времени. "
                                "Отличие от уведомления - автоматическое удаление по зевершении",
                    key="add-timer", function=time_core.notifications_interactor.add_timer,
                    type="notification-adding", required_params=["time"],
                    ignore_following=True, numeric_required=True
                ),
            "delete-notification":
                Command(
                    name="Удаление напоминания",
                    description="Удаление напоминания по заданному порядковому номеру",
                    key="delete-notification", function=time_core.notifications_interactor.delete_notification,
                    type="notification", required_params=["main"], numeric_required=True
                ),
            "nearest-notification":
                Command(
                    name="Поиск ближайшего к текущему моменту уведомления",
                    key="nearest-notification", function=time_core.notifications_interactor.find_nearest_notification,
                    type="notification"
                ),
            "create-stopwatch":
                Command(
                    name="Запуск секундомера",
                    description="Важно, что запуск сразу нескольких секундомеров не поддерживается - "
                                "в любой момент времени может быть запущен только один секундомер",
                    key="create-stopwatch", function=time_core.start_stopwatch, type="stopwatch"
                ),
            "stop-stopwatch":
                Command(
                    name="Остановка секундомера", key="stop-stopwatch", function=time_core.stop_stopwatch,
                    type="stopwatch"
                ),
            "translate":
                Command(
                    name="Перевод текста", description="Перевод заданного текста с русского языка на любой доступный",
                    key="translate", function=translator.translate_text, type="question",
                    required_params=["main", "language"], ignore_following=True
                ),
            "get-volume":
                Command(
                    name="Получение текущего системного уровня громкости", key="get-volume",
                    function=speech_translator.get_volume, type="question"
                ),
            "set-volume":
                Command(
                    name="Изменение текущего системного уровня громкости", key="set-volume",
                    function=speech_translator.set_volume, type="system", required_params=["main"],
                    numeric_required=True
                ),
            "add-TODO":
                Command(
                    name="Добавление заметки на определённую дату",
                    description="Внимание: необходимо указать и день, и месяц. "
                                "Если вы зотите установить заметку просто на какой-то месяц, укажите в качестве дня 1.",
                    key="add-TODO",
                    function=TODO_interactor.add_TODO, type="TODO", required_params=["main", "date"],
                    ignore_following=True, numeric_required=True
                ),
            "find-TODO":
                Command(
                    name="Поиск заметок", description="Можно указать конкретную дату или просто месяц без указания дня",
                    key="find-TODO", function=TODO_interactor.find_TODO, type="TODO", required_params=["date"],
                    numeric_required=True
                ),

            "run-device":
                Command(
                    name="Запуск умного устройства", key="run-device", function=api_actions.light_on,
                    type="devices"
                ),
            "stop-device":
                Command(
                    name="Выключение умного устройства", key="stop-device", function=api_actions.light_off,
                    type="devices"
                )
        }

        if not ready_all(keys=list(self.functions.keys()) + ["__alias__"]):
            raise ImportError("Triggers/alias are not ready. At first you should add alias/triggers for new commands "
                              "and run setup-script 'setup.py'. Make sure that keys in TextProcessor.functions and "
                              "keys in constants.DEFAULT_TRIGGERS are the same.")
        if not ready_all_words(words=AUXILIARY_WORDS):
            raise ImportError("Auxiliary words are not ready. At first you should run setup-script 'setup.py'.")

        triggers = Storage.TRIGGERS
        for key in self.functions.keys():
            for trigger in triggers[key]:
                self.functions[key].triggers.append(trigger)

        self.NAMES = triggers["__alias__"]

    def update_settings(self) -> None:
        """
        Метод обновления настроек текстового процессора.

        :return:
        """

        global_context = GlobalContext()

        triggers = load_all_triggers()
        self.NAMES = triggers["__alias__"]

        self.language_listen = global_context.language_listen

    # В РАЗРАБОТКЕ.
    def _clean_alias(self, command: str) -> str | None:
        """
        Метод, удаляющий обращение к помощнику.

        :param command: ``str``: строка с распознанным текстом.

        :return: Строка с полученной командой.
        """

        for trigger in self.NAMES:
            if not trigger.compatible_langs(lang=self.language_listen):
                continue

            command = command.replace(trigger.text, "", 1).strip()

        return None if command == "" else command

    def _find_extend_info(self, command: str, prefix: str, _ignore_following: bool, _main_required: bool) -> str | None:
        """
        Выделение доп. информации для конкретной команды, заданной параметром ``prefix``.

        :param command: ``str``: строка с распознанным текстом;
        :param prefix: ``str``: текст команды, для которой необходимо найти доп. информацию;
        :param _ignore_following: ``bool``: если ``True``, то игнорируются все последующие команды;
        :param _main_required: ``bool``: требуется ли какая-либо доп. информация.

        :return: Доп. информация к переданной команде / ``None``, если таковой нет.
        """

        command = command[len(prefix) + 1:]

        if _ignore_following:
            return command

        for key, value in self.functions.items():
            for trigger in value.triggers:
                if not trigger.compatible_langs(lang=self.language_listen):
                    continue

                find_result = command.find(trigger.text)
                if find_result == -1:
                    continue

                if find_result == 0 and _main_required:
                    continue

                # если find_result == 0, то пробела, который нужно удалить, перед ним нет, и вычитать единицу не нужно.
                command = command[:(0 if find_result == 0 else find_result - 1)]

        return None if command == "" else command

    def _pick_additive(self, command: str, index: int) -> tuple[Command, int] | None:
        """
        Выделение доп. информации для команды, заданной положением в строке.

        :param command: ``str``: строка с распознанным текстом;
        :param index: ``int``: индекс в строке (нумерация с нуля), с которого, предположительно, начинается команда,
          для которой нужно выделить доп. информацию;

        :return: Если найдена команда, начинающаяся со слова с индексом ``index``, то будет возвращена
        искомая команда с дополнительной информацией, а также число ``shift``, определяющее количество слов в
        выделенной команде (включая доп. информацию).
        """

        command = ' '.join(command.split()[index:])
        for key, value in self.functions.items():
            for trigger in value.triggers:
                if not trigger.check_corresponding(text=command, language=self.language_listen):
                    continue

                additive_info = self._find_extend_info(
                    command=command, prefix=trigger.text, _ignore_following=value.ignore_following,
                    _main_required="main" in self.functions[key].required_params
                )

                out = self.functions[key]
                out.additive["main"] = additive_info

                shift = len(trigger.text.split())
                if additive_info is not None:
                    shift += len(additive_info.split())

                return out, shift

        return None

    # В РАЗРАБОТКЕ.
    def match_command(self, command: str, ignore_all: bool) -> list[Command] | None:
        """
        Поиск команды среди доступных.
        Возвращает список распознанных команд.

        :param command: ``str``: строка с командой;
        :param ignore_all: ``bool``: если ``ignore_all = True``, то учитывается только команда ``ON``.

        :return: Если в тексте не найдено обращения к голосовому помощнику, будет возвращено ``None``.
                 Если обращение к голосовому помощнику найдено, однако не существует запрашиваемой
                 команды, будет возвращен пустой список.
                 Иначе будет возвращен список из распознанных команд.
        """

        command = canonize_text(text=command)

        selected_actions = list()

        # Поиск первого обращения к голосовому помощнику и срез информации ДО него.
        start_pos = None
        for alias in self.NAMES:
            if not alias.compatible_langs(lang=self.language_listen):
                continue

            index = command.find(alias.text)

            if index == -1:
                continue

            if start_pos is None:
                start_pos = index
            else:
                start_pos = min(start_pos, index)

        if start_pos is None:
            return None
        else:
            command = command[start_pos:]

        command = self._clean_alias(command)
        if ignore_all:
            if any(on.text in command for on in self.functions["on"].triggers):
                selected_actions.append(self.functions["on"])
            else:
                return None

            return selected_actions

        if command is None:
            return list()

        command_size = len(command.split())

        it = 0
        while it < command_size:
            picking_result = self._pick_additive(command=command, index=it)
            if picking_result is None:
                it += 1
                continue

            selected_actions.append(picking_result[0])
            it += picking_result[1]

        for i in range(len(selected_actions)):
            selected_actions[i] = parse_info(selected_actions[i], lang=self.language_listen)

        for i in range(len(selected_actions)):
            current_command = selected_actions[i]
            if current_command.key == "create-scenario":
                current_command.additive["subcommands"] = selected_actions[(i + 1):]
                if len(current_command.additive["subcommands"]) == 0:
                    current_command.additive["subcommands"] = None

                del selected_actions[(i + 1):]
                break

        return selected_actions
