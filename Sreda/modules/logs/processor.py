from Sreda.settings import GlobalContext

from Sreda.modules.text.units import Command, Response
from Sreda.modules.logs.units import Log

from Sreda.static.metaclasses import SingletonMetaclass

from datetime import datetime


class Logger(metaclass=SingletonMetaclass):
    """
    ``Singleton``-класс, отвечающий за запись логов.

    **Поля класса:**
        * ``logs_limit`` - ограничение на количество логов;
        * ``logs`` - список логов.

    **Методы класса:**
        * ``update_settings()`` - метод обновления полей класса в соответствии с ``GlobalContext``;
        * ``write()`` - добавить запись в список логов;
        * ``close()`` - закрытие записи и сохранение.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.logs_limit = None
        self.logs = None

    def update_settings(self) -> None:
        """
        Метод обновления настроек логгера.

        :return:
        """

        global_context = GlobalContext()

        self.logs_limit = global_context.logs_limit
        self.logs = global_context.LOGS

        self._shrink()

    def _shrink(self) -> None:
        """
        Удаляет старые логи до того момента, пока количество логов превышает лимит.

        :return:
        """

        while len(self.logs) > self.logs_limit:
            del self.logs[0]

    def write(self, query: Command, response: Response) -> None:
        """
        Логирование пары вида ``[ запрос, ответ ]``.

        :param query: ``Command``: распознанный запрос;
        :param response: ``Response``: ответ на запрос.

        :return:
        """

        self.logs.append(Log(command=query, response=response, time=datetime.now()))

        self._shrink()
