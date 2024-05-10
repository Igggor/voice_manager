from Sreda.settings import GlobalContext

from Sreda.modules.calendar.units import TODONote
from Sreda.modules.text.units import Response

from Sreda.static.metaclasses import SingletonMetaclass

from copy import deepcopy


class TODOInteractor(metaclass=SingletonMetaclass):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(TODOInteractor, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.TODO_limit = None
        self.TODO_list = None

        self.TODO_creation_success = Response(
            text="Заметка успешно сохранена."
        )
        self.empty_TODOs = Response(
            text="Не найдено заметок в заданном отрезке времени."
        )
        self.TODO_find_success = Response(
            text="Найденные заметки. \n"
        )
        self.TODO_overflow_error = Response(
            text="Достигнут лимит количества заметок. Вы можете увеличить его в настройках",
            error=True
        )

    def update_settings(self) -> None:
        global_context = GlobalContext()

        self.TODO_list = global_context.TODO_LIST
        self.TODO_limit = global_context.TODO_limit

        self._shrink()

    def _shrink(self) -> None:
        """
        Удаляет старые заметки до того момента, пока количество заметок превышает лимит.

        :return:
        """

        while len(self.TODO_list) > self.TODO_limit:
            del self.TODO_limit[0]

    def _fix(self) -> None:
        alive = list()

        for note in self.TODO_list:
            if note.is_alive():
                alive.append(note)

        self.TODO_list = alive

    def add_TODO(self, **kwargs) -> Response:
        """
        Метод добавления нового to-do.

        Обязательные агрументы:
            * ``main``: текст того, что нужно сделать;
            * ``month``, ``day``: дата (месяц и день соответственно), на которую ставится to-do заметка.

        :return: Создает новую запись и возвращает фразу-отклик.
        """

        if len(self.TODO_list) + 1 > self.TODO_limit:
            return self.TODO_overflow_error

        self.TODO_list.append(TODONote(
            text=kwargs["main"],
            month=kwargs["date"]["month"],
            day=kwargs["date"]["day"]
        ))

        return self.TODO_creation_success

    def find_TODO(self, **kwargs) -> Response:
        """
        Метод поиска заметок. Основной метод взаимодействия.

        Обязательные агрументы:
            * ``month``: месяц, в котором производится поиск.
        Опциональные аргументы:
            * ``day``: конкретный день, в котором производится поиск. Если не задан,
              будут найдены все заметки данного месяца.

        :return: Возвращает список из найденных заметок (экземпляры класса ``TODONote``).
        """

        self._fix()

        month = kwargs["date"]["month"]
        day = kwargs["date"]["day"]

        found = list()

        if day is None:
            for note in self.TODO_list:
                if note.check_corresponding(month=month):
                    found.append(note)
        else:
            for note in self.TODO_list:
                if note.check_corresponding(day=day, month=month):
                    found.append(note)

        if not len(found):
            return self.empty_TODOs

        response = deepcopy(self.TODO_find_success)
        response.info = ""

        for note in found:
            response.info += note.call()

        return response
