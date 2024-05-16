from Sreda.settings import GlobalContext, load_environment, check_model

from Sreda.modules.time import TimeWorker
from Sreda.modules.logs.processor import Logger
from Sreda.modules.text.processor import TextProcessor
from Sreda.modules.text.units import Response
from Sreda.modules.speech.processor import SpeechTranslator
from Sreda.modules.speech.units import PlayableText
from Sreda.modules.scenarios.processor import ScenarioInteractor
from Sreda.modules.format import check_format, check_recognition
from Sreda.modules.functions import FunctionsCore
from Sreda.modules.translation.processor import Translator
from Sreda.modules.calendar.processor import TODOInteractor
from Sreda.modules.storaging.processor import load_storage

from Sreda.static.metaclasses import SingletonMetaclass

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

        load_environment()
        load_storage()
        check_model()

        self.global_context = GlobalContext()

        self.time_core = TimeWorker()
        self.translator = Translator()

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
        self.functions_core = FunctionsCore()
        self.calendar = TODOInteractor()

        self.greeting = None

        self.hello = [
            Response(
                text="Привет!"
            ),
            Response(
                text="Доброго времени суток."
            ),
            Response(
                text="Рада приветствовать вас."
            ),
            Response(
                text="Рада вас слышать."
            )
        ]
        self.features = Response(
            text=("Сейчас я мало что умею, да и понимаю человека с трудом. "
                  "Но обещаю, буквально через месяц я смогу очень многое!")
        )

        self.thanks = [
            Response(
                text="Я всегда к вашим услугам."
            ),
            Response(
                text="Всегда пожалуйста!"
            ),
            Response(
                text="Рада стараться."
            )
        ]
        self.small_bye = Response(
            text="Была рада помочь."
        )

        self.big_bye = Response(
            text="Всего доброго, буду рада быть полезной снова.",
            do_next=[self.speech_translator.clear_buffer, sys.exit]
        )

        self.update_all()

    def update_all(self) -> None:
        """
        Рекурсивное обновление настроек всех частей приложения. Вызывается при изменении настроек приложения на сервере.

        :return:
        """

        self.greeting = Response(
            text=(f"Приветствую, я твой универсальный голосовой помощник {self.global_context.NAME[0]}.\n"
                  f"Ты можешь узнать о моих возможностях на сайте или просто спросив меня: "
                  f"{self.global_context.NAME[0]}, что ты умеешь?")
        )

        self.time_core.update_settings()
        self.translator.update_settings()
        self.text_processor.update_settings()
        self.speech_translator.update_settings()
        self.scenario_interactor.update_settings()
        self.logger.update_settings()
        self.functions_core.update_settings()
        self.calendar.update_settings()

    def set_ON(self, **_) -> Response:
        """
        Включение голосового помощника.

        :return:
        """

        if self.global_context.ON:
            return self.hello[random.randint(0, len(self.hello) - 1)]

        self.global_context.ON = True
        return self.greeting

    def set_OFF(self, **_) -> Response:
        """
        Частичное выключение голосового помощника (спящий режим).

        :return:
        """

        self.global_context.ON = False
        return self.small_bye

    # Важно! В перспективе здесь не только выход, но, возможно, какое-то сохранение в БД или что-то подобное.
    def exit(self, **_) -> Response:
        """
        Полное выключение голосового помощника.

        :return:
        """

        self.global_context.ON = False
        return self.big_bye

    def features(self, **_) -> Response:
        """
        Запрос о возможностях помощника.

        :return:
        """

        return self.features

    def thanks(self, **_) -> Response:
        """
        Ответ на благодарность.

        :return:
        """

        return self.thanks[random.randint(0, len(self.thanks) - 1)]

    def _periodic_task(self, function, sleeping_time: float) -> None:
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

    def _add_to_output(self, output_text: PlayableText, response: Response, source_language: str = "ru",
                       new: bool = True) -> None:
        """
        Добавляет к исходящему тексту новый элемент.

        :param output_text: ``PlayableText``: экземпляр класса проигрываемого текста;
        :param response: ``Response``: добавляемый объект;
        :param source_language: ``str``: код языка добавляемого текста;
        :param new: ``bool``: выделяется ли в ``output_text`` новый блок под добавляемый текст. Если указано ``False``,
          то подразумевается, что в ``output_text`` добавляется не ``text``, а ``info``.

        :return: Ничего не возвращает, но изменяет ``output_text``, добавляя в него новый элемент.
        """

        # Ядро приложения работает на русском языке, а пользователь, возможно, хочет услышать текст на другом языке.
        # Поэтому текст необходимо переводить (притом не всегда, ведь есть ещё фразы от переводчика), от этого произошло
        # значительное усложнение конструкции.
        if new:
            output_text.add(
                text=self.translator.translate_text_static(
                    text=response.text,
                    source_language=source_language,
                    destination_language=self.global_context.language_speak
                ),

                lang=self.global_context.language_speak
            )
        else:
            output_text.add(
                text=self.translator.translate_text_static(
                    text=response.info,
                    source_language=source_language,
                    destination_language=response.get_language(
                        _undefined=self.global_context.language_speak
                    )
                ),

                lang=response.get_language(
                    _undefined=self.global_context.language_speak
                ),

                new=False
            )

    # В перспективе здесь должно быть собрано несколько функций, в том числе запись логов.
    async def execute(self, selected_actions: list, notification: bool = False) -> None:
        """
        Объединение несколько функций и методов. Выполнение работы от записи логов до
        непосредственного воспроизведения текста.

        Принимает на вход список команд и исполняет их по порядку.

        :param selected_actions: ``list``: список комманд класса ``Command``.
        :param notification: ``bool``: является ли команда уведомлением [по умолчанию = ``False``].

        :return:
        """

        output_text = PlayableText()

        recognition_fail = check_recognition(selected_actions)
        do_next = list()
        if recognition_fail is not None:
            self._add_to_output(output_text=output_text, response=recognition_fail)
            if recognition_fail.info:
                self._add_to_output(output_text=output_text, response=recognition_fail, new=False)
        else:
            if notification:
                query = selected_actions[0]
                response = query.function()

                self.logger.write(query, response)

                self._add_to_output(output_text=output_text, response=response)
                if response.info:
                    self._add_to_output(output_text=output_text, response=response, new=False)

                self.speech_translator.LOCKER.capture_control()

                while not self.speech_translator.LOCKER.can_enter(thread_id=threading.get_native_id()):
                    await asyncio.sleep(0)

                self.speech_translator.speak(output_text)
                return

            for i in range(len(selected_actions)):
                query = selected_actions[i]
                print("[Log: executing]: ", query.additive)

                format_error = check_format(query)
                if format_error is not None:
                    response = format_error
                else:
                    response = query.function(**query.additive)

                    print("[Log: executing]: COMMAND_NAME =", query.name)

                    if response.called_by is None:
                        response.called_by = query

                self.logger.write(query, response)

                self._add_to_output(output_text=output_text, response=response)
                if response.info:
                    self._add_to_output(output_text=output_text, response=response, new=False)

                if response.do_next is not None:
                    do_next = response.do_next

        while not self.speech_translator.LOCKER.available(thread_id=threading.get_native_id()):
            await asyncio.sleep(0)

        self.speech_translator.speak(output_text)

        for action in do_next:
            action()

    # Следующие три функции - оболочки, чтобы можно было адекватно вызывать функции выключения, включения и т.д
    def ON(self) -> None:
        """
        Высокоуровневая функция включения голосового помощника.

        :return:
        """

        asyncio.run(self.execute([self.text_processor.functions["on"]]))

    def OFF(self) -> None:
        """
        Высокоуровневая функция перевода голосового помощника в спящий режим.

        :return:
        """

        asyncio.run(self.execute([self.text_processor.functions["off"]]))

    def EXIT(self) -> None:
        """
        Высокоуровневая функция полного выключения голосового помощника.

        :return:
        """

        asyncio.run(self.execute([self.text_processor.functions["full-off"]]))

    def _listen_command(self) -> None:
        """
        Объединение несколько функций и методов. Выполнение работы от приёма и расшифровки голоса до непосредственного
        выполнения требуемой функции.

        :return:
        """

        recognized_query = self.speech_translator.listen_command()

        # Ядро приложения работает на русском языке, поэтому все команды должны быть переведены на него.

        if recognized_query is None:
            return

        selected_actions = self.text_processor.match_command(recognized_query, not self.global_context.ON)
        print("[Log: match commands]:", recognized_query, selected_actions)
        if selected_actions is None:
            return

        asyncio.run(self.execute(selected_actions))

    def work(self) -> None:
        """
        Основная функция, реализующая работу голосового помощника в целом.

        :return:
        """

        time_thread = threading.Thread(
            target=self._periodic_task,
            args=(self.time_core.check_notifications, self.global_context.notifications_accuracy),
            daemon=True,
            name="Background-TIME"
        )

        time_thread.start()
        while self.global_context.ON:
            self._listen_command()
