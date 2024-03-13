import os
import speech_recognition
from gtts import gTTS


class SpeechTranslator:
    """
    Класс, отвечающий за перевод СТРОКА <-> ГОЛОС (распознавание и произнесение).
    Singleton - pattern
    """
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SpeechTranslator, cls).__new__(cls)
        return cls.__instance

    def __init__(self, __recognizer_threshold: float = 0.5, __microphone_duration: float = 0.5,
                 __language_listen: str = "ru-RU", __language_speak: str = "ru",
                 __recognizer_error_phrase: str = "Команда не распознана"):
        """
        Конструктор класса.
        Инициализирует с необходимыми параметрами микрофон, распознаватель речи, язык работы.

        :param __recognizer_threshold: float;
        :param __microphone_duration: максимальное время прослушивания микрофона;
        :param __language_listen: язык ввода;
        :param __language_speak: язык вывода;
        :param __recognizer_error_phrase: фраза, воспроизводимая при невозможности распознать речь.
        """
        self.MICROPHONE = speech_recognition.Microphone(device_index=1)
        self.MICROPHONE_DURATION = __microphone_duration

        self.RECOGNIZER = speech_recognition.Recognizer()
        self.RECOGNIZER.pause_threshold = __recognizer_threshold

        self.LANGUAGE_LISTEN = __language_listen
        self.LANGUAGE_SPEAK = __language_speak

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
