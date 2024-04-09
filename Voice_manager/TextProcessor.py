from GlobalContext import GlobalContext
from Functions import *
from Classes import *


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
        Инициалиация словаря доступных команд AVAILABLE_COMMANDS, фразы приветствия (при включении) и прощания
        (при выключении).

        Обязательные параметры: системные функции из головного класса VoiceHelper.

        :return:
        """

        not_found = kwargs["not_found"]
        wrong_format = kwargs["wrong_format"]
        set_ON = kwargs["set_ON"]
        features = kwargs["features"]
        thanks = kwargs["thanks"]
        set_OFF = kwargs["set_OFF"]
        safe_exit = kwargs["exit"]

        scenario_interactor = ScenarioInteractor()

        self.NAME = "NAME"

        # В РАЗРАБОТКЕ, все функции помощника должны быть здесь.
        self.functions = {
            "command-not-found":
                Command(
                    name="Команда не распознана.",
                    description="Запрошенная команда не найдена.",
                    key="command-not-found",
                    function=not_found,
                    type="system"
                ),
            "format-error":
                Command(
                    name="Неверный формат команды.",
                    description="Команда распознана корректно, однако нарушен её формат.",
                    key="format-error",
                    function=wrong_format,
                    type="system",
                    additive_required=True,
                    subcommands_required=True
                ),

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
            "off":
                Command(
                    name="Перевод голосового помощника в режим гибернации",
                    description="В режиме сна приложение не закрывается, однако не воспринимает голосовые команды",
                    key="off",
                    function=set_OFF,
                    triggers=["отключись", "отключение"],
                    type="system"
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
            "time":
                Command(
                    name="Получение текущего времени",
                    description="Голосовой помощник получает системное время и озвучивает его",
                    key="time",
                    function=get_time_now,
                    triggers=["сколько времени", "текущее время"],
                    type="question"
                ),
            "date":
                Command(
                    name="Получение текущей даты",
                    description="Голосовой помощник получает текущую дату и озвучивает её",
                    key="date",
                    function=get_date,
                    triggers=["какой сегодня день", "сегодняшняя дата", "текущая дата"],
                    type="question"
                ),
            "course":
                Command(
                    name="Получение текущего курса валют",
                    description="Голосовой помощник получает курс доллара и евро к рублю Центрального Банка России "
                                "(по состоянию на данный момент) и озвучивает его",
                    key="course",
                    function=get_currency_course,
                    triggers=["курс валют"],
                    type="question"
                ),
            "weather-now":
                Command(
                    name="Получение текущей погоды",
                    description="Голосовой помощник получает текущую погоду с заданными параметрами и озвучивает её",
                    key="weather-now",
                    function=get_weather_now,
                    triggers=["какая сейчас погода", "текущая погода"],
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

    # В перспективе будет вызываться при каждом изменении настроек помощника. Это будет гарантировать актуальность
    # аргументов функций, а значит корректность их работы.
    def update_functions_args(self):
        """
        Обновление аргументов функций голосового помощника, задаваемых настройками.

        :return:
        """

        global_context = GlobalContext()
        self.functions["course"].update_args(
            __error_phrase=global_context.COURSE_REQUEST_ERROR_PHRASE
        )

        self.functions["weather-now"].update_args(
            celsium=global_context.weather_temp_celsium,
            mmHg=global_context.weather_pressure_mmHg,
            city=global_context.CITY,
            __error_phrase=global_context.WEATHER_REQUEST_ERROR_PHRASE,
            __not_found_phrase=global_context.WEATHER_NOT_FOUND_PHRASE
        )

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

    def check_format(self, selected_actions: list):
        """
        Проверка формата расшифрованной команды.

        :param selected_actions: list: список команд.

        :return: Обнаруженная ошибка формата или None.
        """

        # Checking forbidden scenario working
        for i in range(1, len(selected_actions)):
            current_command = selected_actions[i]
            if (len(selected_actions) and selected_actions[0].type == "scenario"
                    and current_command.type == "scenario"):
                error = self.functions["format-error"]
                error.additive = ("При создании, удалении или исполнении сценария запрещена любая работа "
                                  "с другими сценариями.")
                error.subcommands = current_command

                return error

        # Checking arguments
        for current_command in selected_actions:
            if current_command.additive_required and current_command.additive is None:
                error = self.functions["format-error"]
                error.additive = "Недостаточно параметров к команде."
                error.subcommands = current_command

                return error

            if current_command.subcommands_required and len(current_command.subcommands) == 0:
                error = self.functions["format-error"]
                error.additive = "Необходимо указать команды для исполнения."
                error.subcommands = current_command

                return error

        return None

    # В РАЗРАБОТКЕ.
    def match_command(self, command: str, ignore_all: bool):
        """
        Поиск команды в словаре AVAILABLE_COMMANDS
        Возвращает список распознанных команд.

        :param command: str: строка с командой;
        :param ignore_all: bool: если ignore_all = True, то учитывается только команда ON.

        :return: Если в тексте не найдено обращения к голосовому помощнику, будет возвращён пустой список.
                 Если обращение к голосовому помощнику найдено, однако в AVAILABLE_COMMANDS не существует запрашиваемой
                 команды, будет возвращено command-not-found.
                 Если хотя бы в одной из команд будет допущена ошибка формата (например, рекурсивное создание сценария
                 в сценарие), то ВСЕ команды будут проигнорированы и возвращён format-error,
                 извещающий об ошибке формата. В случае успешного распознавания команд будет возвращен список
                 из команд.
        """

        selected_actions = list()
        if not any(command.startswith(alias) for alias in self.NAME):
            return selected_actions

        command = self.clean_alias(command)
        if ignore_all:
            if any(on in command for on in self.functions["on"].triggers):
                selected_actions.append(self.functions["on"])

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

        format_verdict = self.check_format(selected_actions)
        if format_verdict is not None:
            return [format_verdict]

        if len(selected_actions) != 0:
            return selected_actions
        else:
            selected_actions.append(self.functions["command-not-found"])
            return selected_actions

# ВЫЗОВ КОМАНД:
#   1. ВКЛЮЧЕНИЕ: Среда, { включись / привет }
#   2. ОТКЛЮЧЕНИЕ: Среда, отключись
#   3. ПОЛНОЕ ОТКЛЮЧЕНИЕ: Среда, отключись полностью
#   4. ТЕКУЩЕЕ ВРЕМЯ: Среда, { текущее время / сколько времени }
#   5. ТЕКУЩАЯ ДАТА: Среда, { какой сегодня день / сегодняшняя дата }
#   6. КУРС ВАЛЮТ: Среда, курс валют
#   7. ТЕКУЩАЯ ПОГОДА: Среда, { какая сейчас погода / текущая погода } { <название населенного пункта> }
#       (если название н.п. не будет названо явно, то будет возвращен прогноз погоды для города по умолчанию -
#       GlobalContext.CITY)
#   8. ДОБАВЛЕНИЕ СЦЕНАРИЯ: Среда, { создай сценарий / добавь сценарий} { <название сценария> }
#       { <команды в стандартном виде, которые будут запущены при выполнении сценария> }
#       ВАЖНО! В сценарии не должно быть никаких действий с другими какими бы то ни было сценариями,
#       нарушение этого правила будет считаться нарушением формата команды.
#   9. ЗАПУСК СЦЕНАРИЯ: Среда, { запусти сценарий / исполни сценарий } { <название сценария> }
#   10. УДАЛЕНИЕ СЦЕНАРИЯ: Среда, удали сценарий { <название сценария> }
