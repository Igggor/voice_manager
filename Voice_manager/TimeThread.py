from Units import Response
from Local import declension
from Constants import MONTH_KEYS
from Metaclasses import SingletonMetaclass
from Notifications import NotificationsInteractor

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
        self.notifications_interactor = NotificationsInteractor()

    def update_settings(self):
        """
        Метод обновления настроек.

        :return:
        """

        self.notifications_interactor.update_settings()

    def get_notifications(self):
        """
        Метод получения списка уведомлений.

        :return: Список уведомлений, состоящий из экземпляров класса ``Notification``.
        """

        return self.notifications_interactor.notifications

    def get_timers(self):
        """
        Метод получения списка таймеров.

        :return: Список таймеров, состоящий из экземпляров класса ``Notification``.
        """

        return self.notifications_interactor.timers

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
    def get_time_static():
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

        current_time = self.get_time_static()

        hours = current_time[0]
        minutes = current_time[1]

        return Response(
            text=f"Сейчас { hours } { declension(hours, 'час') } "
                 f"{ minutes } { declension(minutes, 'минута') }."
        )

    def check_notifications(self):
        """
        Периодичная функция проверки на готовность уведомлений.

        :return: Найденное уведомление, которое нужно воспроизвести (класс ``Notification``), или ``None``.
        """

        print("[Log: time_thread]: notifications detecting...")

        corresponding_notes = list()
        notifications = self.get_notifications()
        for i in range(len(notifications)):
            if notifications[i].check_corresponding():
                corresponding_notes.append(notifications[i])

        corresponding_timers = list()
        timers = self.get_timers()
        for i in range(len(timers)):
            if timers[i].check_corresponding():
                corresponding_timers.append(timers[i])
                self.notifications_interactor.delete_timer(index=i)

        return None if len(corresponding_notes) + len(corresponding_timers) == 0 \
            else corresponding_notes + corresponding_timers
