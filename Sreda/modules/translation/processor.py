from Sreda.settings import GlobalContext

from Sreda.modules.text.units import Response

from Sreda.static.metaclasses import SingletonMetaclass

from googletrans import Translator as GoogleTranslator
from googletrans.client import Timeout
from time import sleep
import httpcore


class Translator(metaclass=SingletonMetaclass):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Translator, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.translation_timeout = None
        self.TRANSLATOR = GoogleTranslator(timeout=Timeout(30.0))

        self.translation_request_error = Response(
            text=("Извините, при запросе перевода текста произошла непредвиденная ошибка. \n"
                  "Повторите запрос позднее."),
            error=True
        )

    def update_settings(self) -> None:
        """
        Метод обновления настроек переводчика.

        :return:
        """

        global_context = GlobalContext()

        if global_context.translation_timeout != self.translation_timeout:
            self.translation_timeout = global_context.translation_timeout
            self.TRANSLATOR = GoogleTranslator(timeout=Timeout(self.translation_timeout))

    def translate_text_static(self, **kwargs) -> str | None:
        """
        Осуществляет перевод текста.

        Обязательные параметры:
            * ``text``: текст для перевода;
            * ``destination_language``: код языка, на который будет переведён текст (генерируется автоматически).
        Опциональные аргументы:
            * ``source_language``: код языка, с которого осуществляется перевод. По умолчанию - ``ru``.
            * ``high_frequency``: является ли запрос выскокочастотным. Если да, то будет включена задержка для
              недопущения искажения и подмены результатов перевода. По умолчанию - ``False``.

        :return: Текст, переведённый на заданный язык. Возвращает **строку**.
        """

        text = kwargs["text"]
        source_language = "auto" if "source_language" not in kwargs.keys() else kwargs["source_language"]
        destination = kwargs["destination_language"]
        high_frequency = False if "high_frequency" not in kwargs.keys() else kwargs["high_frequency"]

        if source_language == destination:
            return text

        try:
            if high_frequency:
                sleep(0.5)

            return self.TRANSLATOR.translate(text=text, src=source_language, dest=destination).text
        except (ValueError, TypeError, AttributeError) as error:
            print(f"Warning: something went wrong while translating text: {error}. "
                  f"Highly likely that it's an API-limits problem. Try to reconnect Internet or change network.")

            return None
        except (httpcore.NetworkError, httpcore.TimeoutException) as error:
            print(f"Warning: something went wrong while translating text: {error}.")

            return None

    def translate_text(self, **kwargs) -> Response:
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

        translated_text = self.translate_text_static(text=text, destination_language=destination)
        if translated_text is not None:
            return Response(
                text="Переведённый текст.",
                info=translated_text,
                extend_lang=destination
            )
        else:
            return self.translation_request_error
