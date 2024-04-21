from GlobalContext import GlobalContext
from Functions import FunctionsCore
from TimeWorker import TimeWorker
from Logger import Logger
from TextProcessor import TextProcessor
from SpeechTranslator import SpeechTranslator
from Scenarios import ScenarioInteractor
from Classes import Command, Response, PlayableText

from random import randint
from threading import Thread
from time import sleep

import threading
import sys
import asyncio


class VoiceHelper:
    """
    Главный класс, отвечающий за связь всех элементов приложения голосового помощника.

    Поля класса:
        * ``global_context - singleton``-класс глобальных настроек;
        * ``functions_core - singleton``-класс функционального ядра;
        * ``time_core - singleton``-класс, отвечающий за работу с временем;
        * ``text_processor - singleton``-класс, отвечающий за преобразование текста в исполняемые команды;

        ``...``

    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(VoiceHelper, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """
        Конструктор класса.

        Инициализируются все составные части приложения (классы).
        """

        self.global_context = GlobalContext()
        self.functions_core = FunctionsCore()
        self.time_core = TimeWorker()
        self.text_processor = TextProcessor(
            set_ON=self.set_ON,
            features=self.features,
            thanks=self.thanks,
            set_OFF=self.set_OFF,
            exit=self.exit
        )

        self.speech_translator = SpeechTranslator()
        self.scenario_interactor = ScenarioInteractor()
        self.logger = Logger()

        self.update_all()

    def update_all(self):
        self.functions_core.update_settings()
        self.logger.update_settings()
        self.time_core.update_settings()
        self.text_processor.update_settings()
        self.speech_translator.update_settings()
        self.scenario_interactor.update_settings()

    # Следующие три функции - оболочки, чтобы можно было адекватно вызывать функции выключения, включения и т.д
    def ON(self):
        asyncio.run(self.execute([self.text_processor.functions["on"]]))

    def OFF(self):
        asyncio.run(self.execute([self.text_processor.functions["off"]]))

    def EXIT(self):
        asyncio.run(self.execute([self.text_processor.functions["full-off"]]))

    def set_ON(self, **kwargs):
        """
        Включение голосового помощника.

        :return:
        """

        if self.global_context.ON:
            return Response(
                text="Привет!"
            )

        self.global_context.ON = True
        return Response(
            text=self.global_context.GREETING_PHRASE
        )

    def set_OFF(self, **kwargs):
        """
        Частичное выключение голосового помощника (спящий режим).

        :return:
        """

        if not self.global_context.ON:
            return Response(
                text=""
            )

        self.global_context.ON = False
        return Response(
            text=self.global_context.SMALL_BYE_PHRASE
        )

    # Важно! В перспективе здесь не только выход, но, возможно, какое-то сохранение в БД или что-то подобное.
    def exit(self, **kwargs):
        """
        Полное выключение голосового помощника.

        :return:
        """

        self.global_context.ON = False

        try:
            self.speech_translator.clear_buffer()
        except OSError:
            pass

        return Response(
            text=self.global_context.BIG_BYE_PHRASE,
            do_next=[self.logger.close, sys.exit]
        )

    def features(self, **kwargs):
        """
        Запрос о возможностях помощника.

        :return:
        """

        return Response(
            text=self.global_context.FEATURES_PHRASE
        )

    def thanks(self, **kwargs):
        """
        Ответ на благодарность.

        :return:
        """

        return Response(
            text=self.global_context.THANKS_PHRASES[randint(0, len(self.global_context.THANKS_PHRASES) - 1)]
        )

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
        if selected_actions is None:
            return

        asyncio.run(self.execute(selected_actions))

    def check_recognition(self, selected_actions: list):
        """
        Проверка корректности распознавания.

        :param selected_actions: ``list``: проверяемый список команд.

        :return: Обнаруженная ошибка, упакованная в класс Response, или None.
        """

        if len(selected_actions) == 0:
            return Response(
                text=self.global_context.RECOGNITION_ERROR_PHRASE,
                is_correct=False
            )

        return None

    def check_format(self, current_command: Command):
        """
        Проверка формата расшифрованной команды.

        :param current_command: ``Command``: проверяемая команда.

        :return: Обнаруженная ошибка формата, упакованная в ``Response``, или ``None``.
        """

        # Checking forbidden scenario working
        if (current_command.type == "scenario" and
                any(sub.type == "scenario" for sub in current_command.subcommands)):
            error = Response(
                type="format-error",
                header=self.global_context.WRONG_COMMAND_FORMAT_PHRASE,
                text="Внутри сценария недопустима работа с другими сценариями.",
                is_correct=False,
                called_by=current_command
            )

            return error

        # Checking arguments
        if current_command.additive_required and current_command.additive is None:
            error = Response(
                type="format-error",
                header=self.global_context.WRONG_COMMAND_FORMAT_PHRASE,
                text="Недостаточно параметров к команде.",
                is_correct=False,
                called_by=current_command
            )

            return error

        if current_command.subcommands_required and len(current_command.subcommands) == 0:
            error = Response(
                type="format-error",
                header=self.global_context.WRONG_COMMAND_FORMAT_PHRASE,
                text="Необходимо указать команды для исполнения.",
                is_correct=False,
                called_by=current_command
            )

            return error

        if current_command.type == "notification-adding":
            error = Response(
                type="format-error",
                header=self.global_context.WRONG_COMMAND_FORMAT_PHRASE,
                text="Заданы неправильные параметры к команде.",
                is_correct=False,
                called_by=current_command
            )

            return error

        return None

    def periodic_task(self, function, sleeping_time: float):
        """
        Статический вспомогательный метод, реализующий работу периодических асинхронных функций.

        :param function: исполняемая периодическая функция;
        :param sleeping_time: ``float``: период исполнения функции.

        :return:
        """

        while True:
            sleep(sleeping_time)
            detecting_result = function()

            if detecting_result is None:
                continue

            executable = self.text_processor.functions["notification"]
            executable.function = detecting_result.call

            asyncio.run(self.execute(selected_actions=[executable], notification=True))

    # В перспективе здесь должно быть собрано несколько функций, в том числе запись логов.
    async def execute(self, selected_actions: list, notification: bool = False):
        """
        Объединение несколько функций и методов. Выполнение работы от записи логов до
        непосредственного воспроизведения текста.

        Принимает на вход список команд и исполняет их по порядку.

        :param selected_actions: ``list``: список комманд класса ``Command``.
        :param notification: ``bool``: является ли команда уведомлением [по умолчанию = ``False``].

        :return:
        """

        output_text = PlayableText()

        recognition_fail = self.check_recognition(selected_actions)
        if recognition_fail is not None:
            output_text.add(recognition_fail.get_speech())
        else:
            if notification:
                query = selected_actions[0]
                response = query.function()

                self.logger.write(query, response)
                output_text.add(response.get_speech())

                print(threading.get_native_id(), self.speech_translator.LOCKER.controlling_thread_id)
                self.speech_translator.LOCKER.capture_control()
                print(threading.get_native_id(), self.speech_translator.LOCKER.controlling_thread_id)

                print("NOTE")
                print(threading.get_native_id(), self.speech_translator.LOCKER.controlling_thread_id, self.speech_translator.LOCKER.can_enter(thread_id=threading.get_native_id()))
                while not self.speech_translator.LOCKER.can_enter(thread_id=threading.get_native_id()):
                    await asyncio.sleep(0)

                self.speech_translator.speak(output_text)

                return

            for i in range(len(selected_actions)):
                query = selected_actions[i]

                format_error = self.check_format(query)
                if format_error is not None:
                    response = format_error
                else:
                    response = query.function(
                        info=query.additive,
                        subcommands=query.subcommands
                    )

                    print("!", response, query.name)
                    if response.type is None:
                        response.type = query.type

                    if response.called_by is None:
                        response.called_by = query

                self.logger.write(query, response)
                output_text.add(response.get_speech())

                if response.do_next is not None:
                    for action in response.do_next:
                        action()

        while not self.speech_translator.LOCKER.available(thread_id=threading.get_native_id()):
            await asyncio.sleep(0)

        self.speech_translator.speak(output_text)

    def work(self):
        """
        Основная функция, реализующая работу голосового помощника в целом.

        :return:
        """

        time_thread = Thread(
            target=self.periodic_task,
            args=(self.time_core.check_notifications, self.global_context.notifications_accuracy),
            daemon=True,
            name="Background-TIME"
        )

        time_thread.start()
        while self.global_context.ON:
            self.listen_command()
