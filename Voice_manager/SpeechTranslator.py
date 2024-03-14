import os
import speech_recognition
from gtts import gTTS
from GlobalContext import *


class SpeechTranslator:
    """
    Класс, отвечающий за перевод СТРОКА <-> ГОЛОС (распознавание и произнесение).
    Singleton - pattern
    """
    __instance = None

    def __new__(cls, __global_context: GlobalContext):
        if cls.__instance is None:
            cls.__instance = super(SpeechTranslator, cls).__new__(cls)
        return cls.__instance

    def __init__(self, __global_context: GlobalContext):
        """
        Конструктор класса.
        Инициализирует с необходимыми параметрами микрофон, распознаватель речи, язык работы.

        :param __global_context: экземпляр класса глобальных настроек GlobalContext
        """
        self.MICROPHONE = speech_recognition.Microphone(device_index=1)
        self.RECOGNIZER = speech_recognition.Recognizer()

        self.MICROPHONE_DURATION = None
        self.LANGUAGE_LISTEN = None
        self.LANGUAGE_SPEAK = None

        self.update_settings(__global_context)

    def update_settings(self, __global_context: GlobalContext):
        """
        Метод обновления настроек микрофона и распознавателя речи.

        :param __global_context: экземпляр класса глобальных настроек GlobalContext
        """
        self.MICROPHONE_DURATION = __global_context.microphone_duration
        self.RECOGNIZER.pause_threshold = __global_context.recognizer_threshold

        self.LANGUAGE_LISTEN = __global_context.language_listen
        self.LANGUAGE_SPEAK = __global_context.language_speak

    # Важно! Запись логов по задумке должна производиться в классе TextProcessor!
    def listen_command(self):
        """
        Метод распознавания текста из речи.

        :return: Возвращает соответствующее строковое значение,
            или, в случае произвольной ошибки, None.
        """
        try:
            with self.MICROPHONE as source:
                self.RECOGNIZER.adjust_for_ambient_noise(source=source, duration=self.MICROPHONE_DURATION)

                audio = self.RECOGNIZER.listen(source=source, timeout=3)

            query = self.RECOGNIZER.recognize_google(audio_data=audio, language=self.LANGUAGE_LISTEN).lower()

            return query
        except:
            return None

    def speak(self, output_text: str, tempo: float = 1.3):
        """
        Метод для синтезации текста в речь.

        :param output_text: текст для синтезации в речь;
        :param tempo: скорость воспроизведения речи.

        :return:
        """
        print(output_text)
        try:
            tts = gTTS(text=output_text, lang=self.LANGUAGE_SPEAK, slow=False, tld="us")
            tts.save('buffer.mp3')

            os.system(f"play buffer.mp3 tempo { tempo }")
        except Exception as ex:
            print(ex)
