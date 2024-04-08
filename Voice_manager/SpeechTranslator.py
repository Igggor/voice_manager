from GlobalContext import GlobalContext

import os
import speech_recognition
from gtts import gTTS


class SpeechTranslator:
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

        self.MICROPHONE = speech_recognition.Microphone(device_index=2)
        self.RECOGNIZER = speech_recognition.Recognizer()

        self.microphone_duration = None
        self.language_listen = None
        self.language_speak = None
        self.listening_timeout = None
        self.speak_speed = None

    def update_settings(self):
        """
        Метод обновления настроек микрофона и распознавателя речи.

        return:
        """

        global_context = GlobalContext()

        self.microphone_duration = global_context.microphone_duration
        self.RECOGNIZER.pause_threshold = global_context.recognizer_threshold

        self.language_listen = global_context.language_listen
        self.language_speak = global_context.language_speak
        self.listening_timeout = global_context.microphone_timeout
        self.speak_speed = global_context.speak_speed

    # Важно! Запись логов по задумке должна производиться в классе TextProcessor!
    def listen_command(self):
        """
        Метод распознавания текста из речи.

        :return: Возвращает соответствующее строковое значение,
            или, в случае произвольной ошибки, None.
        """

        try:
            with self.MICROPHONE as source:
                self.RECOGNIZER.adjust_for_ambient_noise(source=source, duration=self.microphone_duration)
                audio = self.RECOGNIZER.listen(source=source, timeout=self.listening_timeout)
                query = self.RECOGNIZER.recognize_google(audio_data=audio, language=self.language_listen).lower()

            print(query)
            return query
        except Exception as ex:
            print("! ", ex)
            return None

    def speak(self, output_text: str):
        """
        Метод для синтезации текста в речь.

        :param output_text: str: текст для синтезации в речь.

        :return:
        """

        print(output_text)

        def assign_tempo():
            tempo = 1.3
            if len(output_text) > 80:
                tempo = 1.4
            if len(output_text) > 120:
                tempo = 1.45
            if len(output_text) > 150:
                tempo = 1.5

            return max(1.1, min(1.6, tempo * self.speak_speed))

        try:
            tts = gTTS(text=output_text, lang=self.language_speak, tld="com", timeout=10)
            tts.save('buffer.mp3')

            os.system(f"play buffer.mp3 tempo { assign_tempo() }")
        except Exception as ex:
            print(ex)
