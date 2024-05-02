from Units import Response
from Local import declension
from Constants import MONTH_KEYS
from Metaclasses import SingletonMetaclass
from Notifications import NotificationsInteractor
from GlobalContext import GlobalContext

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
        self.stopwatch_initial_time = None

        self.stopwatch_creation_success = None
        self.double_stopwatch_error = None

        self.empty_stopwatch_error = Response(
            text="Невозможно остановить секундомер: в данный момент секундомер не запущен.",
            error=True
        )

        self.stopwatch_finished = Response(
            text="Секундомер успешно завершён."
        )

    def update_settings(self):
        """
        Метод обновления настроек.

        :return:
        """

        global_context = GlobalContext()

        self.notifications_interactor.update_settings()
        self.double_stopwatch_error = Response(
            text=f"Невозможно запустить секундомер: параллельная работа нескольких секундомеров "
                 f"не поддерживается. \n"
                 f"Сначала остановите действующий секундомер, сказав: {global_context.NAME}, останови секундомер.",
            error=True
        )

        self.stopwatch_creation_success = Response(
            text=f"Секундомер запущен. \n"
                 f"В любой момент вы можете остановить его, сказав: {global_context.NAME}, останови секундомер."
        )

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

    def start_stopwatch(self, **kwargs):
        """
        Метод старта секундомера.

        Начинает отсчёт времени (только в случае, если он и так не идёт) и возвращает фразу-отклик.

        :return:
        """

        if self.stopwatch_initial_time is not None:
            return self.double_stopwatch_error

        self.stopwatch_initial_time = datetime.datetime.now()
        return self.stopwatch_creation_success

    def stop_stopwatch(self, **kwargs):
        """
        Метод остановки секундомера.

        Останавливает отсчёт времени (только в том случае, если он идёт) и возвращает фразу-отклик, включающую
        в себя отмеренное время.

        :return:
        """

        if self.stopwatch_initial_time is None:
            return self.empty_stopwatch_error

        moment = datetime.datetime.now()
        delta = moment - self.stopwatch_initial_time

        self.stopwatch_initial_time = None

        response = self.stopwatch_finished

        seconds = int(delta.total_seconds())
        response.info = f" Отмеренное время: {seconds} {declension(seconds, 'секунда')}"

        return response

    @staticmethod
    def get_time_now(**kwargs):
        """
        Функция для получения актуального времени, с точностью до минут.

        :return: Строка в формате ``'Сейчас X часов Y минут.'``
        """

        moment = datetime.datetime.now()

        hours = moment.hour
        minutes = moment.minute

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
        index = 0
        while index < len(self.notifications_interactor.notifications):
            if self.notifications_interactor.notifications[index].check_corresponding():
                corresponding_notes.append(self.notifications_interactor.notifications[index])

            index += 1

        corresponding_timers = list()
        index = 0
        while index < len(self.notifications_interactor.timers):
            if self.notifications_interactor.timers[index].check_corresponding():
                corresponding_timers.append(self.notifications_interactor.timers[index])
                self.notifications_interactor.delete_timer(index=index)

            index += 1

        return None if len(corresponding_notes) + len(corresponding_timers) == 0 \
            else corresponding_notes + corresponding_timers
