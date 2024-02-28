import os
import speech_recognition
from gtts import gTTS


# Класс, отвечающий за перевод СТРОКА <-> ГОЛОС (распознавание и произнесение).
# Singleton - pattern
class SpeechTranslator:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SpeechTranslator, cls).__new__(cls)
        return cls.__instance

    # Конструктор.
    # Опционально принимает на вход вещественные параметры __recognizer_threshold,
    # __microphone_duration, а также строковые параметры __language и __recognizer_error_phrase.
    # Инициализирует с необходимыми параметрами микрофон, распознаватель речи, язык работы.
    def __init__(self, __recognizer_threshold: float = 0.5, __microphone_duration: float = 0.5,
                 __language: str = "ru-RU", __recognizer_error_phrase: str = "Команда не распознана"):
        self.MICROPHONE = speech_recognition.Microphone(device_index=1)
        self.MICROPHONE_DURATION = __microphone_duration

        self.RECOGNIZER = speech_recognition.Recognizer()
        self.RECOGNIZER.pause_threshold = __recognizer_threshold
        self.RECOGNITION_ERROR_PHRASE = __recognizer_error_phrase

        self.LANGUAGE = __language

    # Метод.
    # Прослушивает речь и возвращает соответствующее строковое значение,
    # или, в случае произвольной ошибки, строку "Команда не распознана".
    # Внимание! Запись логов по задумке должна производиться в классе TextProcessor!
    def listenCommand(self):
        try:
            self.RECOGNIZER.adjust_for_ambient_noise(source=self.MICROPHONE, duration=self.MICROPHONE_DURATION)

            audio = self.RECOGNIZER.listen(source=self.MICROPHONE)
            query = self.RECOGNIZER.recognize_google(audio_data=audio, language=self.LANGUAGE).lower()

            return query
        except speech_recognition.UnknownValueError:
            return None
        except:
            return self.RECOGNITION_ERROR_PHRASE

    # Метод.
    # Принимает строку outputText и вещественный параметр tempo
    # и произносит текст, соответсвующий этим параметрам.
    # Внимание! Запись логов по задумке должна производиться в классе TextProcessor!
    def speak(self, outputText: str, tempo: float = 1.3):
        try:
            tts = gTTS(text=outputText, lang=self.LANGUAGE, slow=False, tld="us")
            tts.save('buffer.mp3')

            os.system(f"play buffer.mp3 tempo { tempo }")
        except:
            return None
