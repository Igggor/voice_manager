from Sreda.modules.text.units import Response

from datetime import datetime


class Notification:
    """
    Структура уведомения.
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Инициализирует текст уведомления и его время.

        Обязательные агрументы:
            * ``text``: текст уведомления;
            * ``id``: уникальный идентификатор уведомления.
            * ````

        :return:
        """

        self.text = kwargs["text"]
        self.id = kwargs["id"]

        self.hour = kwargs["hour"]
        self.minute = kwargs["minute"]
        self.second = kwargs["second"]
        self.month = kwargs["month"]
        self.day = kwargs["day"]
        self.timer = kwargs["timer"]

        current_time = datetime.now()
        self.previous_check = current_time

    def check_corresponding(self) -> bool:
        """
        Метод проверки на необходимость воспроизведения данного уведомления прямо сейчас (проверка на то, что его
        время настало).

        :return: ``True`` или ``False``.
        """

        current_time = datetime.now()

        def in_segment() -> bool:
            """
            Проверяет, входит ли время текущего уведомления в отрезок от прошлой проверки до текущего времени.

            :return: ``True`` или ``False``.
            """

            if self.day is None:
                moment = datetime(year=current_time.year, month=current_time.month, day=current_time.day,
                                  hour=self.hour, minute=self.minute, second=self.second)
            else:
                moment = datetime(year=current_time.year, month=self.month, day=self.day,
                                  hour=self.hour, minute=self.minute, second=self.second)

            if self.previous_check <= moment <= current_time:
                return True

            return False

        result = in_segment()

        self.previous_check = current_time

        return result

    def call(self) -> Response:
        """
        Вызов уведомления.

        :return: Уведомление, упакованное в класс ``Response``.
        """

        text = "отсутствует (не указан)." if self.text is None else self.text
        if self.timer:
            return Response(
                text=f"Внимание! Таймер! \n",
                info="Текст таймера: " + text,
                type="notification"
            )
        else:
            return Response(
                text=f"Напоминание (порядковый номер {self.id}). \n",
                info="Текст напоминания: " + text,
                type="notification"
            )
