from TextProcessor import *
from SpeechTranslator import *
from Functions import *
from Classes import *
from random import randint

import sys


class VoiceHelper:
    """
    Главный класс, отвечающий за связь всех элементов приложения.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(VoiceHelper, cls).__new__(cls)
        return cls.__instance

    # В РАЗРАБОТКЕ, все функции помощника должны быть здесь.
    def __init__(self):
        """
        Конструктор класса.

        Инициализируются все составные части приложения (классы), а также словарь functions, где в качестве значений
        хранятся функции из файла Functions.py
        """

        self.global_context = GlobalContext()
        self.text_processor = TextProcessor()
        self.speech_translator = SpeechTranslator()
        self.scenario_interactor = ScenarioInteractor(dict())

        # self.functions хранит класс команд Command; можно обратиться к самой функции ("function") и её аргументам,
        # зависящим от глобальных настроек ("static-args"), также для каждой команды сохранены её доп.параметры.
        self.functions = {
            "С-N-F":
                Command(
                    name="Команда не распознана.",
                    description="Запрошенная команда не найдена.",
                    function=self.not_found,
                    additive_reference=0
                ),
            "F-E":
                Command(
                    name="Неверный формат команды.",
                    description="Команда распознана корректно, однако нарушен её формат.",
                    function=self.wrong_format,
                    additive_reference=2
                ),

            "on":
                Command(
                    name="Включение голосового помощника.",
                    description="Во включенном состоянии глосовой помощник прослушивает команды и исполняет их.",
                    function=self.set_ON,
                    additive_reference=0
                ),
            "features":
                Command(
                    name="Каковы же возможности голосового помощника?",
                    description="Они безграничны!",
                    function=self.features,
                    additive_reference=0
                ),
            "thanks":
                Command(
                    name="Рада стараться.",
                    description="Всегда!",
                    function=self.thanks,
                    additive_reference=0
                ),
            "off":
                Command(
                    name="Перевод голосового помощника в режим гибернации",
                    description="В режиме сна приложение не закрывается, однако не воспринимает голосовые команды",
                    function=self.set_OFF,
                    additive_reference=0
                ),
            "full-off":
                Command(
                    name="Полное выключение голосового помощника",
                    description="Выключение приложения",
                    function=self.exit,
                    additive_reference=0
                ),
            "time":
                Command(
                    name="Получение текущего времени",
                    description="Голосовой помощник получает системное время и озвучивает его",
                    function=get_time_now,
                    additive_reference=0
                ),
            "date":
                Command(
                    name="Получение текущей даты",
                    description="Голосовой помощник получает текущую дату и озвучивает её",
                    function=get_date,
                    additive_reference=0
                ),
            "course":
                Command(
                    name="Получение текущего курса валют",
                    description="Голосовой помощник получает курс доллара и евро к рублю Центрального Банка России "
                                "(по состоянию на данный момент) и озвучивает его",
                    function=get_currency_course,
                    additive_reference=0
                ),
            "weather-now":
                Command(
                    name="Получение текущей погоды",
                    description="Голосовой помощник получает текущую погоду с заданными параметрами и озвучивает её",
                    function=get_weather_now,
                    additive_reference=1
                ),
            "create-scenario":
                Command(
                    name="Создание сценария",
                    description="Создание группы команд с заданным именем, выполняющихся поочередно",
                    function=self.scenario_interactor.add_scenario,
                    additive_reference=2
                ),
            "execute-scenario":
                Command(
                    name="Исполнение сценария",
                    description="Исполнение заданной группы команд, в том порядке, в котором они были даны при создании",
                    function=self.scenario_interactor.execute,
                    additive_reference=2
                ),
            "delete-scenario":
                Command(
                    name="Удаление сценария",
                    description="Удаление группы команд по заданному имени",
                    function=self.scenario_interactor.delete_scenario,
                    additive_reference=2
                )
        }

        self.update_all()

    def update_all(self):
        self.text_processor.update_settings(self.global_context)
        self.speech_translator.update_settings(self.global_context)
        self.scenario_interactor.update_settings(self.global_context)
        self.update_functions_args()
    
    # В перспективе будет вызываться при каждом изменении настроек помощника. Это будет гарантировать актуальность
    # аргументов функций, а значит корректность их работы.
    def update_functions_args(self):
        """
        Обновление аргументов функций голосового помощника, задаваемых настройками.

        :return:
        """

        self.functions["course"].update_args(
            __error_phrase=self.global_context.REQUEST_ERROR_PHRASE
        )

        self.functions["weather-now"].update_args(
            celsium=self.global_context.weather_temp_celsium,
            mmHg=self.global_context.weather_pressure_mmHg,
            city=self.global_context.CITY,
            __error_phrase=self.global_context.REQUEST_ERROR_PHRASE,
            __not_found_phrase=self.global_context.NOT_FOUND_PHRASE
        )

    # Следующие три функции - оболочки, чтобы можно было адекватно вызывать функции выключения, включения и т.д
    def ON(self):
        self.execute([self.functions["on"]])

    def OFF(self):
        self.execute([self.functions["off"]])

    def EXIT(self):
        self.execute([self.functions["full-off"]])

    def set_ON(self, **kwargs):
        """
        Включение голосового помощника.

        :return:
        """

        if self.global_context.ON:
            return

        self.global_context.ON = True
        return self.global_context.GREETING_PHRASE

    def set_OFF(self, **kwargs):
        """
        Частичное выключение голосового помощника (спящий режим).

        :return:
        """

        if not self.global_context.ON:
            return

        self.global_context.ON = False
        return self.global_context.BYE_PHRASE

    # Важно! В перспективе здесь не только выход, но, возможно, какое-то сохранение в БД или что-то подобное.
    def exit(self, **kwargs):
        """
        Полное выключение голосового помощника.

        :return:
        """

        self.global_context.ON = False
        sys.exit()

        pass

    def not_found(self, **kwargs):
        """
        Уведомление о том, что команда не была найдена.

        :return:
        """

        return self.global_context.RECOGNITION_ERROR_PHRASE

    def wrong_format(self, **kwargs):
        """
        Уведомление об ошибке формата команды  с доп. информацией: конкретика об ошибке и название команды,
        в которой она была нарушена.

        :return:
        """

        wrong_command = kwargs["info"][0]
        error = kwargs["info"][1]

        return (self.global_context.WRONG_COMMAND_FORMAT_PHRASE + self.functions[wrong_command].name.lower() + "; \n" +
                error)

    def features(self, **kwargs):
        """
        Полное выключение голосового помощника.

        :return:
        """

        return self.global_context.FEATURES_PHRASE

    def thanks(self, **kwargs):
        """
        Полное выключение голосового помощника.

        :return:
        """

        return self.global_context.THANKS_PHRASES[randint(0, len(self.global_context.THANKS_PHRASES) - 1)]

    def translate_commands(self, commands: list):
        """
        Перевод ключ функции -> функция. Также проверяет соответствие аргументов команд требуемому формату.

        :param commands: list: список пар вида [ключ функции, доп. информация].

        :return: Возвращает список команд (класса Command).
        """
        translated = list()
        if commands[0][0] == "create-scenario":
            command = self.functions["create-scenario"]
            command.additive = commands[0][1]
            command.subcommands = self.translate_commands(commands[1:])

            if command.additive_reference == 0:
                command.additive = None
            if command.additive is None:
                output = self.functions["F-E"]
                output.additive = ["create-scenario", "Необходимо указывать имя создаваемого сценария."]

                return output
            if command.subcommands is None:
                output = self.functions["F-E"]
                output.additive = ["create-scenario", "Необходимо указывать исполняемые функции создаваемого сценария."]

                return output

            translated.append(command)
            return translated

        for key, additive in commands:
            command = self.functions[key]
            command.additive = additive

            if command.additive_reference == 0:
                command.additive = None
            if command.additive_reference == 2 and (command.additive is None):
                output = self.functions["F-E"]
                output.additive = [key, "Недостаточно аргументов для вызова данной команды."]

                return output

            translated.append(command)

        return None if len(translated) == 0 else translated

    def listen_command(self):
        """
        Объединение несколько функций и методов. Выполнение работы от приёма и расшифровки голоса до непосредственного
        выполнения требуемой функции.

        :return:
        """

        recognized_query = self.speech_translator.listen_command()

        if recognized_query is None:
            return

        selected_actions = self.text_processor.match_command(recognized_query, not self.global_context.ON)
        print("[Log]:", recognized_query, selected_actions)
        if selected_actions == [[None, None]]:
            return

        self.execute(self.translate_commands(selected_actions))

    # В перспективе здесь должно быть собрано несколько функций, в том числе запись логов.
    def execute(self, selected_actions: list):
        """
        Объединение несколько функций и методов. Выполнение работы от записи логов (not implemented) до
        непосредственного воспроизведения текста.

        Принимает на вход список команд и исполняет их по порядку.

        :param selected_actions: list: список комманд класса Command.

        :return:
        """

        output_text = ""
        for item in selected_actions:
            output_text += item.function(
                **item.static_args,
                info=item.additive,
                subcommands=item.subcommands
            )

        self.speech_translator.speak(output_text)
