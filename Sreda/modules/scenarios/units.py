from Sreda.modules.text.units import Response


class Scenario:
    """
    Структура сценария.
    """

    def __init__(self, **kwargs):
        """
        Конструктор класса.

        Обязательные аргументы:
            * ``name``: имя (название) сценария;
            * ``functions``: список команд класса ``Command``, которые нужно исполнить при вызове сценария.

        Инициализирует название сценария, а также команды, которые исполняются при его вызове.

        :return:
        """

        self.name = kwargs["name"]
        self.units = kwargs["functions"]

    def execute_scenario(self) -> Response:
        """
        Выполнение сценария.

        :return: Возвращает текст результата выполнения команд сценария.
        """

        output_text = f"Исполняю сценарий { self.name }. \n"
        output_info = str()
        for item in self.units:
            output_info += item.function(**item.additive).get_speech()
            output_info += "\n"

        return Response(
            text=output_text,
            info=output_info
        )
