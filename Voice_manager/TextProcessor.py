from GlobalContext import GlobalContext


class TextProcessor:
    """
    Класс, отвечающий за сопоставление текста с необходимой командой.
    Singleton - pattern
    """
    __instance = None

    def __new__(cls, __global_context: GlobalContext):
        if cls.__instance is None:
            cls.__instance = super(TextProcessor, cls).__new__(cls)
        return cls.__instance

    def __init__(self, __global_context: GlobalContext):
        """
        Конструктор класса.
        Инициалиация словаря доступных команд AVAILABLE_COMMANDS, фразы приветствия (при включении) и прощания
        (при выключении).

        :param __global_context: глобальные настройки.
        """

        # AVAILABLE_COMMANDS должен быть переработан (наверное)
        self.AVAILABLE_COMMANDS = {
            "alias": ["Name"],
            "commands": {
                "thanks": ["спасибо", "благодарю"],
                "full-off": ["отключись полностью", 'отключить полностью'],
                "off": ["отключись"],
                "on": ["привет", "включись"],
                "time": ["текущее время", "сколько времени"],
                "date": ["какой сегодня день", "сегодняшняя дата"],
                "weather-now": ["какая сейчас погода", "текущая погода"],
                "course": ["курс валют"],
                "features": ["что ты умеешь"]
            }
        }

        self.update_settings(__global_context)

    def update_settings(self, __global_context: GlobalContext):
        """
        Метод обновления настроек текстового процессора.

        :param __global_context: экземпляр класса глобальных настроек GlobalContext
        """

        self.AVAILABLE_COMMANDS["alias"] = [__global_context.NAME.lower()]

    # В РАЗРАБОТКЕ.
    def clean_alias(self, command: str):
        """
        Метод, удаляющий обращение к помощнику.

        :param command: str: строка с распознанным текстом.

        :return: Строка с полученной командой.
        """
        for item in self.AVAILABLE_COMMANDS['alias']:
            command = command.replace(item, "").strip()

        return None if command == "" else command

    def clean_extend(self, command: str, prefix: str):
        """
        Выделение доп. информации для конкретной команды, заданной параметром prefix.

        :param command: str: строка с распознанным текстом.
        :param prefix: str: текст команды, для которой необходимо найти доп. информацию

        :return: Доп. информация к этой команде / None, если таковой нет.
        """
        command = command[len(prefix) + 1:]

        for key, value in self.AVAILABLE_COMMANDS["commands"].items():
            for v in value:
                find_result = command.find(v)
                if find_result == -1:
                    continue

                # если find_result == 0, то пробела, который нужно удалить, перед ним нет, и вычитать единицу не нужно.
                command = command[:(0 if find_result == 0 else find_result - 1)]

        return None if command == "" else command

    def pick_additive(self, command: str, index: int):
        """
        Выделение доп. информации для команды, заданной положением в строке.

        :param command: str: строка с распознанным текстом.
        :param index: int: индекс в строке (нумерация с нуля), с которого, предположительно, начинается команда,
                           для которой нужно выделить доп. информацию

        :return: Если найдена команда, начинающаяся со слова с индексом index, то будет возвращена пара вида
                 [ ключ команды, доп. информация к этой команде / None, если таковой нет ]. В противном случае будет
                 возвращено None.
        """
        command = ' '.join(command.split()[index:])
        for key, value in self.AVAILABLE_COMMANDS["commands"].items():
            for v in value:
                if not command.startswith(v):
                    continue

                additive_info = self.clean_extend(command, v)
                return [key, additive_info]

        return None

    # Важно! В этом методе планируется реализовать запись логов
    # (примерный вид: запрос -> что подошло -> доп. информация).
    # В РАЗРАБОТКЕ.
    def match_command(self, command: str, ignore_all: bool):
        """
        Поиск команды в словаре AVAILABLE_COMMANDS
        Возвращает пару вида {ключ команды; дополнительные данные}.

        :param command: строка с командой
        :param ignore_all: bool-метка. Если ignore_all = True, то учитывается только команда ON

        :return: Если в тексте не найдено обращения к голосовому помощнику, будет возвращено [[ None; None ]].
                 Если обращение к голосовому помощнику найдено, однако в AVAILABLE_COMMANDS не существует запрашиваемой
                 команды, будет возвращён служебный ключ [[ "С-N-F", None ]]. В случае успешного распознавания команд
                 будет возвращен список из пар вида
                 [ ключ команды, доп. информация к этой команде / None, если таковой нет ].
        """
        selected_actions = list()
        if not any(command.startswith(alias) for alias in self.AVAILABLE_COMMANDS["alias"]):
            selected_actions.append([None, None])
            return selected_actions

        command = self.clean_alias(command)
        if ignore_all:
            if any(on in command for on in self.AVAILABLE_COMMANDS["commands"]["on"]):
                selected_actions.append(["on", None])
            else:
                selected_actions.append([None, None])

            return selected_actions

        command_size = len(command.split())
        for it in range(command_size):
            picking_result = self.pick_additive(command, it)
            if picking_result is None:
                continue

            selected_actions.append(picking_result)

        print("[Log]:", selected_actions)
        if len(selected_actions) != 0:
            return selected_actions
        else:
            selected_actions.append(["С-N-F", None])
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
#       GlobalContext.CITY
