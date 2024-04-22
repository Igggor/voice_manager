from context import GlobalContext
from classes import Response, Notification
from local import declension
from constants import MONTH_KEYS
from meta import SingletonMetaclass
from constants import get_phrase

import datetime


class TimeWorker(metaclass=SingletonMetaclass):
    """
    Класс, отвечающий за работу с временем.

    **Поля класса:**
        * ``notifications_limit`` - ограничение на количество созданный напоминаний;
        * ``notifications_accuracy`` - точность (вещественное число, в секундах), с которой будет происходит поиск
          напоминаний, таймеров и т.д. Иными словами, представляет периодичность поиска напоминаний;
        * ``notifications`` - список напоминаний;

    **Методы класса:**
        * ``update_settings()`` - обновление настроек класса;
        * ``get_time_static()`` - низкоуровневая функция получения текущего времени;

        ``...``
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(TimeWorker, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.notifications_limit = None
        self.notifications_accuracy = None
        self.notifications = None

    def update_settings(self):
        """
        Метод обновления настроек.

        :return:
        """

        global_context = GlobalContext()

        self.notifications_limit = global_context.notifications_limit
        self.notifications_accuracy = global_context.notifications_accuracy
        self.notifications = global_context.NOTIFICATIONS

    @staticmethod
    def get_date(**kwargs):
        """
        Функция для получения актуальной даты.

        :return: Строка, обозначающая дату, в формате "Сегодня ..."
        """

        current_date = datetime.date.today()

        day = current_date.day
        month = current_date.month
        year = current_date.year

        return Response(
            text=f"Сегодня { day } { MONTH_KEYS[month - 1] } { year } года."
        )

    @staticmethod
    def __get_time_static():
        """
        Получение текущего времени с точностью до секунд.

        :return: Список вида [час, минута, секунда].
        """

        current_time = datetime.datetime.now()

        hours = current_time.hour
        minutes = current_time.minute
        seconds = current_time.second

        return [hours, minutes, seconds]

    def get_time_now(self, **kwargs):
        """
        Функция для получения актуального времени, с точностью до минут.

        :return: Строка в формате ``'Сейчас X часов Y минут.'``
        """

        current_time = self.__get_time_static()

        hours = current_time[0]
        minutes = current_time[1]

        return Response(
            text=f"Сейчас { hours } { declension(hours, 'час') } "
                 f"{ minutes } { declension(minutes, 'минута') }."
        )

    def add_notification(self, **kwargs):
        """
        Метод добавления нового уведомления.

        Обязательные агрументы (передаются через ``info``):
            * ``text``: текст уведомления;
            * ``hour``: час;
            * ``minute``: минута.
        Опциональные аргументы (передаются через ``info``):
            * ``second``: секунда [по умолчанию = ``0``].

        :return: Создает новое уведомление и возвращает фразу-отклик.
        """

        current_id = len(self.notifications) + 1
        if "second" not in kwargs.keys():
            self.notifications.append(Notification(
                text=kwargs["text"],
                id=current_id,
                hour=kwargs["hour"],
                minute=kwargs["minute"]
            ))
        else:
            self.notifications.append(Notification(
                text=kwargs["text"],
                id=current_id,
                hour=kwargs["hour"],
                minute=kwargs["minute"],
                second=kwargs["second"]
            ))

        return Response(
            text=get_phrase("NOTIFICATION_CREATION_SUCCESS") +
            f" Созданное уведомление имеет порядковый номер {current_id}."
        )

    def add_timer(self, **kwargs):
        raise NotImplementedError

    def delete_notification(self, **kwargs):
        """
        Метод удаления уведомления.

        Обязательные аргументы (передаются через ``info``):
            * ``id``: порядковый номер уведомления.

        :return: Удаляет уведомление и возвращает фразу-отклик.
        """

        note_id = kwargs["id"]
        if note_id < len(self.notifications):
            del self.notifications[note_id]

            for i in range(len(self.notifications)):
                self.notifications[i].id = i

            return get_phrase("NOTIFICATION_DELETION_SUCCESS")
        else:
            return get_phrase("NOTIFICATION_DELETION_ERROR")

    def find_nearest_notification(self):
        """
        Поиск ближайшего напоминания к текущему моменту.

        :return: Возвращает текст ближайшего уведомления, обернутый в экземляр класса ``Response``.
        """

        today = datetime.datetime.today()

        def distance(note: Notification):
            """
            Функция нахождения расстояния между моментами времени в секундах.

            :param note: ``Notification``: экземпляр класса напоминания, для которого функция найдёт расстояние
            от текущего момента (в секундах).

            :return: Целочисленное значение - расстояние от текущего момента
                до следующего воспроизведения данного уведомления.
            """

            moment = datetime.datetime(today.year, today.month, today.day, note.hour, note.minute, note.second)

            delta = (moment - datetime.datetime.now()).total_seconds()
            return delta

        try:
            x = min(self.notifications, key=distance)

            response = x.call()
            response.header = "Ближайшее уведомление: \n" + response.header

            return response
        except ValueError:
            response = Response(
                text=get_phrase("EMPTY_NOTIFICATIONS_ERROR"),
                is_correct=False,
                called_by=self.find_nearest_notification
            )

            return response

    def check_notifications(self):
        """
        Периодичная функция проверки на готовность уведомлений.

        :return: Найденное уведомление, которое нужно воспроизвести (класс ``Notification``), или ``None``.
        """

        if len(self.notifications) == 0:
            self.notifications = [
                Notification(text="тестовое уведомление выключить утюг", id=1, hour=16, minute=19, second=20),
                Notification(text="уведомление номер два включить чайник", id=2, hour=19, minute=8, second=35)
            ]

            print(self.find_nearest_notification())

        print("[Log]: notifications detecting...")
        current_time = self.__get_time_static()

        for note in self.notifications:
            if note.check_corresponding(
                    current_hour=current_time[0],
                    current_minute=current_time[1],
                    current_second=current_time[2]
            ):
                return note

        return None
