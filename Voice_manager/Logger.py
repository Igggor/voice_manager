from GlobalContext import GlobalContext
from Units import Command, Response
from Metaclasses import SingletonMetaclass


class Logger(metaclass=SingletonMetaclass):
    """
    Класс, отвечающий за запись логов.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Logger, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.logs_limit = None
        self.logs = None

    def update_settings(self):
        """
        Метод обновления настроек логгера.

        :return:
        """

        global_context = GlobalContext()

        self.logs_limit = global_context.logs_limit
        self.logs = global_context.LOGS

    def write(self, query: Command, response: Response):
        """
        Логирование пары вида ``[ запрос, ответ ]``.

        :param query: ``Command``: распознанный запрос;
        :param response: ``Response``: ответ на запрос;

        :return:
        """

        self.logs.append([query, response])

        while len(self.logs) > self.logs_limit:
            del self.logs[0]

    def close(self):
        """
        Метод глобального сохранения логов. Вызывается при закрытии приложения.

        :return:
        """

        global_context = GlobalContext()
        global_context.LOGS = self.logs
