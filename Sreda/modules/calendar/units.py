from Sreda.static.constants import MONTH_KEYS

from datetime import datetime


class TODONote:
    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Обязательные агрументы:
            * ``text``: текст того, что нужно сделать;
            * ``month``, ``day``: дата (месяц и день соответственно), на которую ставится to-do заметка.

        Инициализирует текст заметки и её дату.

        :return:
        """

        self.text = kwargs["text"]
        self.month = kwargs["month"]
        self.day = kwargs["day"]

        self.timestamp = datetime.now()

    def is_alive(self) -> bool:
        now = datetime.now()
        moment = datetime(year=self.timestamp.year, month=self.month, day=self.day, hour=23, minute=59, second=59)
        if moment < self.timestamp:
            moment = datetime(
                year=self.timestamp.year + 1, month=self.month, day=self.day, hour=23, minute=59, second=59
            )

        # moment - последний момент "жизни" заметки
        if moment < now:
            return False

        return True

    def check_corresponding(self, month: int, day: int = None) -> bool:
        if day is None:
            if month == self.month:
                return True

            return False

        if day == self.day and month == self.month:
            return True

        return False

    def call(self) -> str:
        return f"Дата: {self.day} {MONTH_KEYS[self.month - 1]}. Текст: {self.text[0].upper() + self.text[1:]} \n"
