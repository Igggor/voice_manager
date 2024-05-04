from Metaclasses import SingletonMetaclass
from Units import Response
from GlobalContext import GlobalContext

from googletrans import Translator as GoogleTranslator
from googletrans.client import Timeout
import httpcore


class Translator(metaclass=SingletonMetaclass):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Translator, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.translation_timeout = None
        self.TRANSLATOR = None

        self.translation_request_error = Response(
            text=("Извините, при запросе перевода текста произошла непредвиденная ошибка. \n"
                  "Повторите запрос позднее."),
            error=True
        )

    def update_settings(self):
        global_context = GlobalContext()

        if global_context.translation_timeout != self.translation_timeout:
            self.translation_timeout = global_context.translation_timeout
            self.TRANSLATOR = GoogleTranslator(timeout=Timeout(self.translation_timeout))

    def translate_text_static(self, **kwargs):
        """
        Осуществляет перевод текста.

        Обязательные параметры:
            * ``text``: текст для перевода;
            * ``language``: код языка, на который будет переведён текст (генерируется автоматически).
        Опциональные аргументы:
            * ``source_language``: код языка, с которого осуществляется перевод.

        :return: Текст, переведённый на заданный язык. Возвращает **строку**.
        """

        text = kwargs["text"]
        source_language = "auto" if "source_language" not in kwargs.keys() else kwargs["source_language"]
        destination = kwargs["language"]

        if source_language == destination:
            return text

        return self.TRANSLATOR.translate(text=text, src=source_language, dest=destination).text

    def translate_text(self, **kwargs):
        """
        Осуществляет перевод текста c русского на иностранный.

        Обязательные параметры:
            * ``main``: текст для перевода;
            * ``language``: код языка, на который будет переведён текст (генерируется автоматически).

        :return: Текст, переведённый на заданный язык.
                 В случае непредвиденной ошибки возвращает строку с соответствующим предупреждением.
                 Возвращает **объект класса Response**.
        """

        text = kwargs["main"]
        destination = kwargs["language"]

        try:
            return Response(
                text="Переведённый текст.",
                info=self.translate_text_static(text=text, language=destination),
                extend_lang=destination
            )
        except (ValueError, httpcore.NetworkError, httpcore.TimeoutException):
            return self.translation_request_error
