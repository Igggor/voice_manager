from GlobalContext import GlobalContext
from Units import PlayableText
from Metaclasses import SingletonMetaclass

import threading
import os
import speech_recognition
from gtts import gTTS


class StreamLocker:
    def __init__(self):
        """
        Конструктор класса.

        :return:
        """

        self.controlling_thread_id = None
        self.collision = False

    def free(self):
        """
        Метод, проверяющий, является ли ввод-вывод в данный момент свободным,
        то есть не контролируемым ни одним из потоков.

        :return: ``True`` или ``False``.
        """

        return self.controlling_thread_id is None

    def capture_control(self):
        """
        Метод форсированной передачи контроля голосового ввода-вывода текущему потоку.

        По завершении блока текста немедленно прерывает воспроизведение, без возможности возобновления.
        После этого передает контроль над вводом-выводом потоку, вызвавшему метод.

        :return:
        """

        if not self.free():
            self.collision = True

        self.lock(force=True)

    def lock(self, force: bool = False):
        """
        Метод блокирования голосового ввода-вывода: передает контроль над вводом-выводом потоку, вызвавшему метод.

        Если ``force = True``, то ввод-вывод будет принудительно передан новому потоку,
        даже если сейчас он заблокирован.

        По умолчанию ``force = False``.

        При блокировке ввода-вывода поток становится ``контролирующим`` для класса ``SpeechTranslator``.

        :return: В случае успешной блокировки потока ввода-вывода будет возвращено ``True``.
            В противном случае при попытке заблокировать уже заблокированный поток будет возвращено ``False``.
        """

        if force:
            self.controlling_thread_id = threading.get_native_id()
            return True

        if self.free() or self.is_controller(thread_id=threading.get_native_id()):
            self.controlling_thread_id = threading.get_native_id()
            return True

        return False

    def unlock(self, force: bool = False):
        """
        Разблокирует голосовой ввод-вывод.

        Если ``force = True``, то ввод-вывод будет разблокирован, даже если он был заблокирован другим потоком.

        В противном случае разблокировать ввод-вывод может только контролирующий поток.

        По умолчанию ``force = False``.

        :return: В случае успешной разблокировки потока ввода-вывода будет возвращено ``True``.
            В случае вызова метода неконтролирующим потоком при установленном ``force = False``
            ввод-вывод разблокирован не будет, при этом будет возвращено ``False``.
        """

        if self.free():
            return True

        if force:
            self.controlling_thread_id = None
            return True
        if self.is_controller(thread_id=threading.get_native_id()):
            self.controlling_thread_id = None
            return True

        return False

    def get_controller(self):
        """
        Метод, возвращающий ``id`` контролирующего потока.

        :return: уникальный (нативный) идентификатор контролирующего потока, выданный операционной системой.
        """

        return self.controlling_thread_id

    def is_controller(self, thread_id: int):
        """
        Метод, проверяющий, является ли поток c ``native_id = thread_id`` контролирующим.

        :param thread_id: ``int``: нативный ``id`` потока, для которого проверяется доступность ввода-вывода.

        :return: ``True`` или ``False``.
        """

        return self.controlling_thread_id == thread_id

    def available(self, thread_id: int):
        """
        Метод, проверяющий, может ли в данный момент поток c ``native_id = thread_id`` получить доступ к вводу-выводу.

        :param thread_id: ``int``: нативный ``id`` потока, для которого проверяется доступность ввода-вывода.

        :return: ``True`` или ``False``.
        """

        return self.is_controller(thread_id=thread_id) or self.free()

    def can_enter(self, thread_id: int):
        """
        Метод, проверяющий, доступен ли перехват управления голосовым вводом-выводом потоку c ``native_id = thread_id``.

        :param thread_id: ``int``: нативный ``id`` потока, для которого проверяется доступность ввода-вывода.

        :return: ``True`` или ``False``.
        """

        return (self.is_controller(thread_id=thread_id) or self.free()) and not self.collision


class SpeechTranslator(metaclass=SingletonMetaclass):
    """
    Класс, отвечающий за перевод СТРОКА <-> ГОЛОС (распознавание и произнесение).
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SpeechTranslator, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        """
        Конструктор класса.
        Инициализирует с необходимыми параметрами микрофон, распознаватель речи, язык работы.

        :return:
        """

        self.MICROPHONE = speech_recognition.Microphone()
        self.RECOGNIZER = speech_recognition.Recognizer()

        self.microphone_duration = None
        self.phrase_limit = None

        self.language_listen = None
        self.language_speak = None
        self.listening_timeout = None
        self.speak_speed = None

        self.LOCKER = StreamLocker()

    def update_settings(self):
        """
        Метод обновления настроек микрофона и распознавателя речи.

        return:
        """

        global_context = GlobalContext()

        self.microphone_duration = global_context.microphone_duration
        self.RECOGNIZER.pause_threshold = global_context.recognizer_threshold
        self.phrase_limit = global_context.phrase_timeout

        self.language_listen = global_context.language_listen
        self.language_speak = global_context.language_speak
        self.listening_timeout = global_context.microphone_timeout
        self.speak_speed = global_context.speak_speed

    def listen_command(self):
        """
        Метод распознавания текста из речи.

        :return: Возвращает соответствующее строковое значение,
            или, в случае произвольной ошибки, ``None``.
        """

        if not self.LOCKER.available(thread_id=threading.get_native_id()):
            return None

        try:
            with self.MICROPHONE as source:
                self.RECOGNIZER.adjust_for_ambient_noise(source=source, duration=self.microphone_duration)
                audio = self.RECOGNIZER.listen(source=source, timeout=self.listening_timeout,
                                               phrase_time_limit=self.phrase_limit)
                query = self.RECOGNIZER.recognize_vosk(audio_data=audio, language=self.language_listen)

            print("[Log: listen command]:", query[14:len(query) - 3])
            return query[14:len(query) - 3]
        except (speech_recognition.UnknownValueError, speech_recognition.WaitTimeoutError) as error:
            print(f"Warning: something went wrong while recognizing voice: {error}")
            return None

    @staticmethod
    def prepare_text(output_text: str, lang: str, index: int):
        """
        С помощью ``gTTS-API`` переводит текст в речь и сохраняет её в виде файла ``.mp3``.

        :param output_text: ``str``: блок ответа голосового помощника;
        :param lang: ``str``: код языка вопспроизведения;
        :param index: ``int``: индекс блока (фрагмента).

        :return:
        """

        try:
            tts = gTTS(text=output_text, lang=lang, tld="com", timeout=10)
            tts.save(f"buffer/{index}.mp3")
        except OSError as error:
            print(f"Warning: something went wrong while saving file with index {index}: {error}")
        except (RuntimeError, ValueError, AssertionError) as error:
            print(f"Warning: something went wrong preparing text to playing: {error}")

    @staticmethod
    def play_text(index: int, tempo: float):
        try:
            os.system(f"play buffer/{index}.mp3 tempo {tempo}")
        except OSError as error:
            print(f"Warning: something went wrong while playing file with index {index}: {error}")

    def speak(self, output: PlayableText):
        """
        Метод для синтезации текста в речь.

        :param output: ``PlayableText``: текст для синтезации в речь.

        :return:
        """

        locked = self.LOCKER.lock()
        if not locked:
            print("Warning: stream was not locked, but the first phrase will be played.")

        self.clear_buffer()

        speech = output.get_normal_text()
        print(speech)

        def assign_tempo():
            tempo = 1.25
            if len(speech) > 80:
                tempo = 1.3
            if len(speech) > 120:
                tempo = 1.4
            if len(speech) > 150:
                tempo = 1.45

            return max(1.1, min(1.6, tempo * self.speak_speed))

        resulting_tempo = assign_tempo()
        blocks = output.get_straight_blocks()
        print(blocks)

        for i in range(len(blocks)):
            self.prepare_text(output_text=blocks[i]["source"], lang=blocks[i]["language"], index=i)

        for i in range(len(blocks)):
            if i > 0 and not self.LOCKER.is_controller(thread_id=threading.get_native_id()):
                self.LOCKER.collision = False
                return

            self.play_text(index=i, tempo=resulting_tempo)

        if not self.LOCKER.is_controller(thread_id=threading.get_native_id()):
            self.LOCKER.collision = False
            return

        self.LOCKER.collision = False

        unlocked = self.LOCKER.unlock()
        if not unlocked:
            print("Warning: stream was not unlocked. High probability of unexpected behavior")

    @staticmethod
    def clear_buffer():
        """
        Метод очистки буфера воспроизведения.

        Удаляет все временные файлы в папке ``buffer``.

        :return:
        """

        try:
            os.system("rm buffer/*")
        except OSError as error:
            print(f"Warning: something went wrong while removing files from buffer: {error}")
