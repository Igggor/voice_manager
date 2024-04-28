from GlobalContext import GlobalContext
from TimeThread import TimeWorker
from Logger import Logger
from TextProcessing import TextProcessor
from SpeechTranslator import SpeechTranslator
from Scenarios import ScenarioInteractor
from Units import Response, PlayableText
from Metaclasses import SingletonMetaclass
from FormatChecking import FormatChecker
from Functions import FunctionsCore

from time import sleep

import threading
import sys
import asyncio
import random


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
        self.format_checker = FormatChecker()
        self.functions_core = FunctionsCore()

        self.greeting = None
        self.small_bye = None
        self.big_bye = None
        self.features = None
        self.thanks = None

        self.update_all()

    def update_all(self):
        """
        Рекурсивное обновление настроек всех частей приложения. Вызывается при изменении настроек приложения.

        :return:
        """

        self.global_context.update_settings()
        self.global_context.big_bye.do_next = [self.logger.close, sys.exit]

        self.time_core.update_settings()
        self.text_processor.update_settings()
        self.speech_translator.update_settings()
        self.scenario_interactor.update_settings()
        self.logger.update_settings()
        self.format_checker.update_settings()
        self.functions_core.update_settings()

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
        return self.global_context.greeting

    def set_OFF(self, **kwargs):
        """
        Частичное выключение голосового помощника (спящий режим).

        :return:
        """

        if not self.global_context.ON:
            return None

        self.global_context.ON = False
        return self.global_context.small_bye

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

        return self.global_context.big_bye

    def features(self, **kwargs):
        """
        Запрос о возможностях помощника.

        :return:
        """

        return self.global_context.features

    def thanks(self, **kwargs):
        """
        Ответ на благодарность.

        :return:
        """

        return self.global_context.thanks[random.randint(0, len(self.global_context.thanks) - 1)]

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

            actions = list()
            for note in detecting_result:
                executable = self.text_processor.functions["notification"]
                executable.function = note.call

                actions.append(executable)

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

        recognition_fail = self.format_checker.check_recognition(selected_actions)
        if recognition_fail is not None:
            output_text.add(recognition_fail.get_speech())
        else:
            if notification:
                query = selected_actions[0]
                response = query.function()

                self.logger.write(query, response)
                output_text.add(response.get_speech())

                self.speech_translator.LOCKER.capture_control()

                while not self.speech_translator.LOCKER.can_enter(thread_id=threading.get_native_id()):
                    await asyncio.sleep(0)

                self.speech_translator.speak(output_text)
                return

            for i in range(len(selected_actions)):
                query = selected_actions[i]
                print("[Log: executing]: ", query.additive)

                format_error = self.format_checker.check_format(query)
                if format_error is not None:
                    response = format_error
                else:
                    response = query.function(**query.additive)

                    print("!", response, query.name)

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
        print("[Log: match commands]:", recognized_query, selected_actions)
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
