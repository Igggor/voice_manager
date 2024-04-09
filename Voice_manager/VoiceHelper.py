from TextProcessor import *
from SpeechTranslator import *
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

    def __init__(self):
        """
        Конструктор класса.

        Инициализируются все составные части приложения (классы), а также словарь functions, где в качестве значений
        хранятся функции из файла Functions.py
        """

        self.global_context = GlobalContext()
        self.text_processor = TextProcessor(
            not_found=self.not_found,
            wrong_format=self.wrong_format,
            set_ON=self.set_ON,
            features=self.features,
            thanks=self.thanks,
            set_OFF=self.set_OFF,
            exit=self.exit
        )

        self.speech_translator = SpeechTranslator()
        self.scenario_interactor = ScenarioInteractor()

        self.update_all()

    def update_all(self):
        self.text_processor.update_settings()
        self.speech_translator.update_settings()
        self.scenario_interactor.update_settings()
        self.text_processor.update_functions_args()

    # Следующие три функции - оболочки, чтобы можно было адекватно вызывать функции выключения, включения и т.д
    def ON(self):
        self.execute([self.text_processor.functions["on"]])

    def OFF(self):
        self.execute([self.text_processor.functions["off"]])

    def EXIT(self):
        self.execute([self.text_processor.functions["full-off"]])

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

        Обязательные параметры:
            * info: поясняющий текст ошибки;
            * subcommands: экземпляр класса Command - той команды, формат которой нарушен.

        :return:
        """

        wrong_command = kwargs["subcommands"]
        error = kwargs["info"]

        return (self.global_context.WRONG_COMMAND_FORMAT_PHRASE + wrong_command.name.lower() + "; \n" +
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

        self.execute(selected_actions)

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
        for i in range(len(selected_actions)):
            item = selected_actions[i]
            response = item.function(
                **item.static_args,
                info=item.additive,
                subcommands=item.subcommands
            )

            output_text += response
            if i < len(selected_actions) - 1:
                output_text += "\n\n"

        self.speech_translator.speak(output_text)
