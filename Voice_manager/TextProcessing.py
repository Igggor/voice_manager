from GlobalContext import GlobalContext
from Functions import FunctionsCore
from TimeThread import TimeWorker
from Units import Command
from Scenarios import ScenarioInteractor
from Metaclasses import SingletonMetaclass
from Parser import parse_info
from Local import replace_numbers
from SpeechTranslator import SpeechTranslator
from Translation import Translator


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

        scenario_interactor = ScenarioInteractor()
        time_core = TimeWorker()
        functions_core = FunctionsCore()
        speech_translator = SpeechTranslator()
        translator = Translator()

        self.NAME = None

        # В РАЗРАБОТКЕ, все функции помощника должны быть здесь.
        # Каждая функция возвращает структуру Response.
        self.functions = {
            "notification":
                Command(
                    name=None, description=None, key="notification", function=None, type="system-call"
                ),

            "on":
                Command(
                    name="Включение голосового помощника.",
                    description="Во включенном состоянии глосовой помощник прослушивает команды и исполняет их.",
                    key="on", function=set_ON, triggers=["привет", "включись", "включение"], type="system"
                ),
            "features":
                Command(
                    name="Возможности голосового помощника.",
                    key="features", function=features, triggers=["что ты умеешь", "возможности"], type="question"
                ),
            "thanks":
                Command(
                    name="Рада стараться.",
                    key="thanks", function=thanks, triggers=["спасибо", "благодарю"], type="question"
                ),
            "full-off":
                Command(
                    name="Полное выключение голосового помощника",
                    description="Выключение приложения",
                    key="full-off", function=safe_exit,
                    triggers=["отключись полностью", "отключить полностью", "полное отключение"], type="system"
                ),
            "off":
                Command(
                    name="Перевод голосового помощника в режим гибернации",
                    description="В режиме сна приложение не закрывается, однако не воспринимает голосовые команды",
                    key="off", function=set_OFF, triggers=["отключись", "отключение"], type="system"
                ),
            "time":
                Command(
                    name="Получение текущего времени",
                    description="Голосовой помощник получает системное время и озвучивает его",
                    key="time", function=time_core.get_time_now, triggers=["сколько времени", "текущее время"],
                    type="question"
                ),
            "date":
                Command(
                    name="Получение текущей даты",
                    description="Голосовой помощник получает текущую дату и озвучивает её",
                    key="date", function=time_core.get_date,
                    triggers=["какой сегодня день", "сегодняшняя дата", "текущая дата"], type="question"
                ),
            "course":
                Command(
                    name="Получение текущего курса валют",
                    description="Голосовой помощник получает курс доллара и евро к рублю Центрального Банка России "
                                "(по состоянию на данный момент) и озвучивает его",
                    key="course", function=functions_core.get_currency_course, triggers=["курс валют"], type="question"
                ),
            "weather-now":
                Command(
                    name="Получение текущей погоды",
                    description="Голосовой помощник получает текущую погоду с заданными параметрами и озвучивает её",
                    key="weather-now", function=functions_core.get_weather_now,
                    triggers=["какая сейчас погода", "текущая погода", "погода"], type="question"
                ),
            "create-scenario":
                Command(
                    name="Создание сценария",
                    description="Создание группы команд с заданным именем, выполняющихся поочередно",
                    key="create-scenario", function=scenario_interactor.add_scenario,
                    triggers=["создай сценарий", "добавь сценарий", "добавление сценария"], type="scenario",
                    required_params=["main", "subcommands"], ignore_following=True
                ),
            "execute-scenario":
                Command(
                    name="Исполнение сценария",
                    description="Исполнение заданной группы команд, "
                                "в том порядке, в котором они были даны при создании",
                    key="execute-scenario", function=scenario_interactor.execute,
                    triggers=["запусти сценарий", "исполни сценарий", "исполнение сценария"], type="scenario",
                    required_params=["main"]
                ),
            "delete-scenario":
                Command(
                    name="Удаление сценария",
                    description="Удаление группы команд по заданному имени",
                    key="delete-scenario", function=scenario_interactor.delete_scenario,
                    triggers=["удали сценарий", "удаление сценария"], type="scenario",
                    required_params=["main"]
                ),
            "add-notification":
                Command(
                    name="Добавление напоминания",
                    description="Добавление напоминания с заданным текстом и временем запуска",
                    key="add-notification", function=time_core.notifications_interactor.add_notification,
                    triggers=["добавь уведомление", "добавь напоминание", "создай уведомление", "создай напоминание"],
                    type="notification-adding", required_params=["time"], ignore_following=True
                ),
            "add-timer":
                Command(
                    name="Добавление таймера",
                    description="Добавление таймера на заданное количество времени. "
                                "Отличие от уведомления - автоматическое удаление по зевершении",
                    key="add-timer", function=time_core.notifications_interactor.add_timer,
                    triggers=["добавь таймер", "создай таймер"], type="notification-adding", required_params=["time"],
                    ignore_following=True
                ),
            "delete-notification":
                Command(
                    name="Удаление напоминания",
                    description="Удаление напоминания по заданному порядковому номеру",
                    key="delete-notification", function=time_core.notifications_interactor.delete_notification,
                    triggers=["удали напоминание", "удали уведомление"], type="notification", required_params=["main"]
                ),
            "nearest-notification":
                Command(
                    name="Поиск ближайшего к текущему моменту уведомления",
                    key="nearest-notification", function=time_core.notifications_interactor.find_nearest_notification,
                    triggers=["ближайшее уведомление", "ближайшее напоминание"], type="notification"
                ),
            "create-stopwatch":
                Command(
                    name="Запуск секундомера",
                    description="Важно, что запуск сразу нескольких секундомеров не поддерживается - "
                                "в любой момент времени может быть запущен только один секундомер",
                    key="create-stopwatch", function=time_core.start_stopwatch,
                    triggers=["создай секундомер", "запусти секундомер", "поставь секундомер"], type="stopwatch"
                ),
            "stop-stopwatch":
                Command(
                    name="Остановка секундомера", key="stop-stopwatch", function=time_core.stop_stopwatch,
                    triggers=["останови секундомер", "заверши секундомер"], type="stopwatch"
                ),
            "translate":
                Command(
                    name="Перевод текста", description="Перевод заданного текста с русского языка на любой доступный",
                    key="translate", function=translator.translate_text,
                    triggers=["переведи текст", "переведи", "сделай перевод"], type="question",
                    required_params=["main", "language"], ignore_following=True
                ),
            "get-volume":
                Command(
                    name="Получение текущего системного уровня громкости", key="get-volume",
                    function=speech_translator.get_volume, triggers=["текущий уровень громкости", "текущая громкость"],
                    type="question"
                ),
            "set-volume":
                Command(
                    name="Изменение текущего системного уровня громкости", key="set-volume",
                    function=speech_translator.set_volume,
                    triggers=["измени уровень громкости", "установи уровень громкости",
                              "измени громкость", "установи громкость"],
                    type="system", required_params=["main"]
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

        :param command: ``str``: строка с распознанным текстом.

        :return: Строка с полученной командой.
        """

        for item in self.NAME:
            command = command.replace(item, "", 1).strip()

        return None if command == "" else command

    def find_extend_info(self, command: str, prefix: str, ignore_following: bool):
        """
        Выделение доп. информации для конкретной команды, заданной параметром ``prefix``.

        :param command: ``str``: строка с распознанным текстом;
        :param prefix: ``str``: текст команды, для которой необходимо найти доп. информацию;
        :param ignore_following: ``bool``: если ``True``, то игнорируются все последующие команды.

        :return: Доп. информация к переданной команде / ``None``, если таковой нет.
        """

        command = command[len(prefix) + 1:]

        if ignore_following:
            return command

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

        :param command: ``str``: строка с распознанным текстом;
        :param index: ``int``: индекс в строке (нумерация с нуля), с которого, предположительно, начинается команда,
                           для которой нужно выделить доп. информацию.

        :return: Если найдена команда, начинающаяся со слова с индексом ``index``, то будет возвращена
        искомая команда с дополнительной информацией, а также число ``shift``, определяющее количество слов в
        выделенной команде (включая доп. информацию).
        """

        command = ' '.join(command.split()[index:])
        for key, value in self.functions.items():
            for v in value.triggers:
                if not command.startswith(v):
                    continue

                additive_info = self.find_extend_info(
                    command=command, prefix=v, ignore_following=value.ignore_following
                )

                out = self.functions[key]
                out.additive["main"] = additive_info

                shift = len(v.split())
                if additive_info is not None:
                    shift += len(additive_info.split())

                return [out, shift]

        return None

    # В РАЗРАБОТКЕ.
    def match_command(self, command: str, ignore_all: bool):
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

        command = replace_numbers(text=command)

        selected_actions = list()

        # Поиск первого обращения к голосовому помощнику и срез информации ДО него.
        start_pos = None
        for alias in self.NAME:
            index = command.find(alias)

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

        command = self.clean_alias(command)
        if ignore_all:
            if any(on in command for on in self.functions["on"].triggers):
                selected_actions.append(self.functions["on"])
            else:
                return None

            return selected_actions

        command_size = len(command.split())

        it = 0
        while it < command_size:
            picking_result = self.pick_additive(command, it)
            if picking_result is None:
                it += 1
                continue

            selected_actions.append(picking_result[0])
            it += picking_result[1]

        for i in range(len(selected_actions)):
            selected_actions[i] = parse_info(selected_actions[i])

        for i in range(len(selected_actions)):
            current_command = selected_actions[i]
            if current_command.key == "create-scenario":
                current_command.additive["subcommands"] = selected_actions[(i + 1):]
                if len(current_command.additive["subcommands"]) == 0:
                    current_command.additive["subcommands"] = None

                del selected_actions[(i + 1):]
                break

        return selected_actions
