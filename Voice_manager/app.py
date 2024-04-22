from context import GlobalContext
from constants import get_phrase
from time_thread import TimeWorker
from logger import Logger
from text_processing import TextProcessor
from speech import SpeechTranslator
from scenarios import ScenarioInteractor
from classes import Command, Response, PlayableText
from meta import SingletonMetaclass

from time import sleep

import threading
import sys
import asyncio


class VoiceHelper(metaclass=SingletonMetaclass):
    """
    Главный ``singleton``-класс, отвечающий за связь всех элементов приложения голосового помощника.

    **Поля класса:**
        * ``global_context - singleton``-класс глобальных настроек;
        * ``time_core - singleton``-класс, отвечающий за работу с временем;
        * ``text_processor - singleton``-класс, отвечающий за преобразование текста в исполняемые команды;
        * ``speech_translator - singleton``-класс, отвечающий за перевод из голосовой информации в текст и наоборот;
        * ``scenario_interactor - singleton``-класс, отвечающий за работу со сценариями;
        * ``logger - singleton``-класс, отвечающий за логирование;

    **Публичные методы класса:**
        * ``update_all()`` - рекурсивное обновление настроек всех частей приложения.
          Вызывается при изменении настроек приложения.
        * ``ON(), OFF(), EXIT()`` - функции,
          предназначенные для **запроса** включения, выключения частичного и полного соответственно;
        * ``listen_command()`` - функция прослушивания информации, сочетающая в себе несколько задач,
          в том числе само прослушивание и распознавание;
        * ``work()`` - головная функция, объединяющая в себя всю работу голосового помощника.
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
            text=get_phrase("GREETING")
        )

    def set_OFF(self, **kwargs):
        """
        Частичное выключение голосового помощника (спящий режим).

        :return:
        """

        if not self.global_context.ON:
            return None

        self.global_context.ON = False
        return Response(
            text=get_phrase("SMALL_BYE")
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
            text=get_phrase("BIG_BYE"),
            do_next=[self.logger.close, sys.exit]
        )

    @staticmethod
    def features(**kwargs):
        """
        Запрос о возможностях помощника.

        :return:
        """

        return Response(
            text=get_phrase("FEATURES")
        )

    @staticmethod
    def thanks(**kwargs):
        """
        Ответ на благодарность.

        :return:
        """

        return Response(
            text=get_phrase("THANKS")
        )

    @staticmethod
    def check_recognition(selected_actions: list):
        """
        Проверка корректности распознавания.

        :param selected_actions: ``list``: проверяемый список команд.

        :return: Обнаруженная ошибка, упакованная в класс Response, или None.
        """

        if len(selected_actions) == 0:
            return Response(
                text=get_phrase("RECOGNITION_ERROR"),
                is_correct=False
            )

        return None

    @staticmethod
    def check_format(current_command: Command):
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
                header=get_phrase("WRONG_COMMAND_FORMAT_ERROR"),
                text="Внутри сценария недопустима работа с другими сценариями.",
                is_correct=False,
                called_by=current_command
            )

            return error

        # Checking arguments
        if current_command.additive_required and current_command.additive is None:
            error = Response(
                type="format-error",
                header=get_phrase("WRONG_COMMAND_FORMAT_ERROR"),
                text="Недостаточно параметров к команде.",
                is_correct=False,
                called_by=current_command
            )

            return error

        if current_command.subcommands_required and len(current_command.subcommands) == 0:
            error = Response(
                type="format-error",
                header=get_phrase("WRONG_COMMAND_FORMAT_ERROR"),
                text="Необходимо указать команды для исполнения.",
                is_correct=False,
                called_by=current_command
            )

            return error

        if current_command.type == "notification-adding":
            error = Response(
                type="format-error",
                header=get_phrase("WRONG_COMMAND_FORMAT_ERROR"),
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

    def update_all(self):
        """
        Рекурсивное обновление настроек всех частей приложения. Вызывается при изменении настроек приложения.

        :return:
        """

        self.logger.update_settings()
        self.time_core.update_settings()
        self.text_processor.update_settings()
        self.speech_translator.update_settings()
        self.scenario_interactor.update_settings()

    # Следующие три функции - оболочки, чтобы можно было адекватно вызывать функции выключения, включения и т.д
    def ON(self):
        """
        Высокоуровневая функция включения голосового помощника.

        :return:
        """

        asyncio.run(self.execute([self.text_processor.functions["on"]]))

    def OFF(self):
        """
        Высокоуровневая функция перевода голосового помощника в спящий режим.

        :return:
        """

        asyncio.run(self.execute([self.text_processor.functions["off"]]))

    def EXIT(self):
        """
        Высокоуровневая функция полного выключения голосового помощника.

        :return:
        """

        asyncio.run(self.execute([self.text_processor.functions["full-off"]]))

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

    def work(self):
        """
        Основная функция, реализующая работу голосового помощника в целом.

        :return:
        """

        time_thread = threading.Thread(
            target=self.periodic_task,
            args=(self.time_core.check_notifications, self.global_context.notifications_accuracy),
            daemon=True,
            name="Background-TIME"
        )

        time_thread.start()
        while self.global_context.ON:
            self.listen_command()
