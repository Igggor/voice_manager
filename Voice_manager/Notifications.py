from Metaclasses import SingletonMetaclass
from GlobalContext import GlobalContext
from Units import Notification
from Responses import ResponsesHandler
from Constants import MONTH_KEYS
from Local import declension

from datetime import datetime, timedelta


class NotificationsInteractor(metaclass=SingletonMetaclass):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(NotificationsInteractor, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.timers_limit = None
        self.notifications_limit = None
        self.notifications_accuracy = None

        self.notifications = None
        self.timers = None

        self.timer_creation_success = None
        self.note_creation_success = None
        self.note_deletion_success = None
        self.notes_list_empty_error = None
        self.notes_list_overflow_error = None
        self.timers_list_overflow_error = None
        self.note_not_found_error = None

    def renumerate(self):
        """
        Переприсваивает уведомлениям корректные ``id``.

        :return:
        """

        for i in range(len(self.notifications)):
            self.notifications[i].id = i

    def shrink(self):
        """
        Удаляет старые уведомления до того момента, пока количество уведомлений превышает лимит.

        :return:
        """

        while len(self.notifications) > self.notifications_limit:
            del self.notifications[0]

        self.renumerate()

    def update_settings(self):
        """
        Метод обновления настроек.

        :return:
        """

        global_context = GlobalContext()

        self.notifications_limit = global_context.notifications_limit
        self.timers_limit = global_context.timers_limit
        self.notifications_accuracy = global_context.notifications_accuracy

        self.notifications = global_context.NOTIFICATIONS
        self.timers = global_context.TIMERS

        handler = ResponsesHandler()

        self.timer_creation_success = handler.timer_creation_success
        self.note_creation_success = handler.note_creation_success
        self.note_deletion_success = handler.note_deletion_success
        self.notes_list_empty_error = handler.notes_list_empty_error
        self.notes_list_overflow_error = handler.notes_list_overflow_error
        self.timers_list_overflow_error = handler.timers_list_overflow_error
        self.note_not_found_error = handler.note_not_found_error

    def add_notification(self, **kwargs):
        """
        Метод добавления нового уведомления.

        Обязательные агрументы:
            * ``text``: текст уведомления;
            * ``hour``: час;
            * ``minute``: минута;
            * ``second``: секунда.
        Опциональные аргументы:
            * ``month``, ``day``: дата (месяц и день соответственно), когда будет запущено уведомление.

        :return: Создает новое уведомление и возвращает фразу-отклик.
        """

        current_id = len(self.notifications) + 1
        if current_id > self.notifications_limit:
            return self.notes_list_overflow_error

        self.notifications.append(Notification(
            text=kwargs["main"],
            id=current_id,
            hour=kwargs["time"]["hours"],
            minute=kwargs["time"]["minutes"],
            second=kwargs["time"]["seconds"],
            month=(None if kwargs["date"] is None else kwargs["date"]["month"]),
            day=(None if kwargs["date"] is None else kwargs["date"]["day"]),
            timer=False
        ))

        response = self.note_creation_success
        response.info = f"Созданное уведомление имеет порядковый номер {current_id}."
        return response

    def add_timer(self, **kwargs):
        """
        Метод добавления нового таймера.

        Обязательные агрументы:
            * ``text``: текст таймера;
            * ``hour``: длительность в часах;
            * ``minute``: длительность в минутах;
            * ``second``: длительность в секундах.

        :return: Создает новое таймер и возвращает фразу-отклик.
        """

        current_id = len(self.timers) + 1
        if current_id > self.timers_limit:
            return self.timers_list_overflow_error

        moment = datetime.now()
        moment += timedelta(
            hours=kwargs["time"]["hours"],
            minutes=kwargs["time"]["minutes"],
            seconds=kwargs["time"]["seconds"]
        )

        print(moment.hour, moment.minute, moment.second)
        self.timers.append(Notification(
            text=kwargs["main"],
            id=current_id,
            hour=moment.hour,
            minute=moment.minute,
            second=moment.second,
            month=moment.month,
            day=moment.day,
            timer=True
        ))

        response = self.timer_creation_success
        response.info = (f"Он завершится { moment.day } { MONTH_KEYS[moment.month - 1] } в "
                         f"{ moment.hour } { declension(moment.hour, 'час') } "
                         f"{ moment.minute } { declension(moment.minute, 'минута') } "
                         f"{ moment.second } {declension(moment.second, 'секунда') }")
        return response

    def delete_notification(self, **kwargs):
        """
        Метод удаления уведомления.

        Обязательные аргументы:
            * ``id``: порядковый номер уведомления.

        :return: Удаляет уведомление и возвращает фразу-отклик.
        """

        note_id = int(kwargs["main"])
        if note_id < len(self.notifications):
            del self.notifications[note_id]

            for i in range(len(self.notifications)):
                self.notifications[i].id = i

            return self.note_deletion_success
        else:
            return self.note_not_found_error

    def find_nearest_notification(self, **kwargs):
        """
        Поиск ближайшего напоминания к текущему моменту.

        :return: Возвращает текст ближайшего уведомления, обернутый в экземляр класса ``Response``.
        """

        current_time = datetime.now()

        def distance(note: Notification):
            """
            Функция нахождения расстояния между моментами времени в секундах.

            :param note: ``Notification``: экземпляр класса напоминания, для которого функция найдёт расстояние
            от текущего момента (в секундах).

            :return: Целочисленное значение - расстояние от текущего момента
                до следующего воспроизведения данного уведомления.
            """

            if note.month is None or note.day is None:
                moment = datetime(current_time.year, current_time.month, current_time.day,
                                  note.hour, note.minute, note.second)

                if moment > current_time:
                    moment += timedelta(days=1)
            else:
                moment = datetime(current_time.year, note.month, note.day,
                                  note.hour, note.minute, note.second)

                if moment > current_time:
                    moment += timedelta(days=365)

            delta = (moment - datetime.now()).total_seconds()
            return delta

        try:
            x = min(self.notifications, key=distance)

            response = x.call()
            response.text = "Ближайшее напоминание. \n" + response.text

            return response
        except ValueError:
            return self.notes_list_empty_error


