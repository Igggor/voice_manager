from Metaclasses import SingletonMetaclass
from GlobalContext import GlobalContext
from Units import Notification, Response
from Constants import MONTH_KEYS
from Local import declension

from datetime import datetime, timedelta
from copy import deepcopy


class NotificationsInteractor(metaclass=SingletonMetaclass):
    """
    ``Singleton``-класс, отвечающий за взаимодействие с напоминаниями и таймерами.

    **Поля класса:**
        * ``timers_limit`` - ограничение на количество установленных таймеров;
        * ``notifications_limit`` - ограничение на количество установленных уведомлений;
        * ``accuracy`` - точность воспроизведения напоминаний и таймеров;
        * ``notifications`` - список напоминаний;
        * ``timers`` - список таймеров;
        * ``timer_creation_success`` - ``Response``-объект, возвращаемый при успешном создании таймера;
        * ``note_creation_success`` - ``Response``-объект, возвращаемый при умпешном создании напоминания;
        * ``note_deletion_success`` - ``Response``-объект, возвращаемый при успешном удалении напоминания;
        * ``notes_list_empty_error`` - ``Response``-объект, возвращаемый при невозможности выполнить операцию
          над пустым списком напоминаний;
        * ``notes_list_overflow_error`` - ``Response``-объект, возвращаемый при превышении ``notifications_limit``;
        * ``timers_list_overflow_error`` - ``Response``-объект, возвращаемый при превышении ``timers_limit``;
        * ``note_not_found_error`` - ``Response``-объект, возвращаемый при невозможности найти запрашиваемое
          напоминание;

    **Методы класса:**
        * ``renumerate()`` - переприсваивает уведомлениям корректные ``id``;
        * ``shrink()`` - путём удаления старых напоминаний/таймеров сжимает списки напоминаний и таймеров до лимита;
        * ``update_settings()`` - метод обновления полей класса в соответствии с ``GlobalContext``;
        * ``add_notification()`` - метод добавления нового напоминания;
        * ``add_timer()`` - метод добавления нового таймера;
        * ``delete_notification()`` - метод удаления напоминания по его ``id``;
        * ``delete_timer()`` - метод удаления таймера по его ``id``;
        * ``find_nearest_notification()`` - находит ближайшее к текущему моменту уведомление.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(NotificationsInteractor, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.timers_limit = None
        self.notifications_limit = None
        self.accuracy = None

        self.notifications = None
        self.timers = None

        self.note_creation_success = Response(
            text="Напоминание успешно создано. \n"
        )
        self.timer_creation_success = Response(
            text="Таймер успешно создан. \n"
        )
        self.note_deletion_success = Response(
            text="Напоминание успешно удалено. Первое из оставшихся уведомлений теперь имеет номер 1."
        )

        self.note_not_found_error = Response(
            text=("Не удалось удалить напоминание с заданным порядковым номером.\n"
                  "Похоже, такого напоминания не существует. Уточните команду и повторите попытку."),
            error=True
        )
        self.notes_list_empty_error = Response(
            text="Невозможно найти ближайшее напоминание: список уведомлений пуст.",
            error=True
        )
        self.notes_list_overflow_error = None
        self.timers_list_overflow_error = Response(
            text="Достигнут лимит количества установленных таймеров. \n"
                 "Вы можете увеличить его в настройках.",
            error=True
        )

    def renumerate(self):
        """
        Переприсваивает уведомлениям корректные ``id``.

        :return:
        """

        for i in range(len(self.notifications)):
            self.notifications[i].id = i + 1

        for i in range(len(self.timers)):
            self.timers[i].id = i + 1

    def shrink(self):
        """
        Удаляет старые уведомления до того момента, пока количество уведомлений превышает лимит.

        :return:
        """

        while len(self.notifications) > self.notifications_limit:
            del self.notifications[0]
        while len(self.timers) > self.timers_limit:
            del self.timers[0]

        self.renumerate()

    def update_settings(self):
        """
        Метод обновления настроек.

        :return:
        """

        global_context = GlobalContext()

        self.notifications_limit = global_context.notifications_limit
        self.timers_limit = global_context.timers_limit
        self.accuracy = global_context.notifications_accuracy

        self.notifications = global_context.NOTIFICATIONS
        self.timers = global_context.TIMERS

        self.notes_list_overflow_error = Response(
            text=f"Достигнут лимит количества напоминаний. \n"
                 f"Вы можете увеличить его в настройках или удалить произвольное напоминание, сказав: "
                 f"{global_context.NAME}, удали напоминание. \n"
                 f"Не забудьте указать номер удаляемого напоминания.",
            error=True
        )

        self.shrink()

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

        hour = kwargs["time"]["hours"]
        minute = kwargs["time"]["minutes"]
        second = kwargs["time"]["seconds"]
        month = None if kwargs["date"] is None else kwargs["date"]["month"]
        day = None if kwargs["date"] is None else kwargs["date"]["day"]

        self.notifications.append(Notification(
            text=kwargs["main"],
            id=current_id,
            hour=hour,
            minute=minute,
            second=second,
            month=month,
            day=day,
            timer=False
        ))

        if kwargs["date"] is None:
            moment = datetime.now()
            potential = datetime(year=moment.year, month=moment.month, day=moment.day, hour=hour,
                                 minute=minute, second=second)

            day_key = "сегодня" if potential > moment else "завтра"

            response = deepcopy(self.note_creation_success)
            response.info = (f"Оно будет запущено {day_key} в {hour} {declension(hour, 'час')} "
                             f"{minute} {declension(minute, 'минута')} "
                             f"{second} {declension(second, 'секунда') }. "
                             f"Созданное уведомление имеет порядковый номер {current_id}.")
            return response
        else:
            response = deepcopy(self.note_creation_success)
            response.info = (f"Оно будет запущено {day} {MONTH_KEYS[month - 1]} "
                             f"в {hour} {declension(hour, 'час')} "
                             f"{minute} {declension(minute, 'минута')} "
                             f"{second} {declension(second, 'секунда')}. "
                             f"Созданное уведомление имеет порядковый номер {current_id}.")
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

        response = deepcopy(self.timer_creation_success)
        response.info = (f"Он завершится {moment.day} {MONTH_KEYS[moment.month - 1]} в "
                         f"{moment.hour} {declension(moment.hour, 'час')} "
                         f"{moment.minute} {declension(moment.minute, 'минута')} "
                         f"{moment.second} {declension(moment.second, 'секунда')}.")
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

            self.renumerate()

            return self.note_deletion_success
        else:
            return self.note_not_found_error

    def delete_timers(self, indexes: list):
        """
        Метод удаления таймеров. Не может быть вызван пользователем.

        :param indexes: ``list``: список из индексов тех таймеров, которые необходимо удалить.

        :return:
        """

        # Благодаря той особенности списка таймеров, что поддерживается инвариант "индекс в массиве + 1 = id таймера",
        # можно удалять используя не явный индекс в массиве, который при удалении будет меняться, а id таймера.
        # После всех удалений для поддержания вышеописанного инварианта таймеры должны быть перенумерованы.

        for index in indexes:
            for i in range(len(self.timers)):
                if self.timers[i].id == index:
                    del self.timers[i]
                    break

        self.renumerate()

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
