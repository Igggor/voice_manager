from Sreda.environment import Environment

from Sreda.modules.logs.units import Log
from Sreda.modules.text.units import Response

from Sreda.static.metaclasses import SingletonMetaclass

import requests


class APIProcessor(metaclass=SingletonMetaclass):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(APIProcessor, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.url = "https://test.igreeda.keenetic.pro/API"

        self.KEY = Environment.NATIVE_API_KEY
        self.HTTP_TIMEOUT = 5
        self.RETRY = 3

    def _get(self, table: str, **kwargs) -> requests.Response | None:
        """
        Метод GET-запроса.

        :param table: ``str``: рабочая таблица.

        :return: Результат запроса / ``None``.
        """

        params = {"key": self.KEY}
        params.update(kwargs)

        _url = f"{self.url}/{table}"

        try:
            response = requests.get(url=_url, params=params, timeout=self.HTTP_TIMEOUT)
            return response
        except requests.exceptions.RequestException:
            return None

    def _post(self, table: str, **kwargs) -> requests.Response | None:
        """
        Метод POST-запроса.

        :param table: ``str``: рабочая таблица.

        :return: Результат запроса.
        """

        getparams = {"key": self.KEY}

        body = {"params": kwargs}

        _url = f"{self.url}/{table}"

        try:
            response = requests.post(url=_url, json=body, params=getparams, timeout=self.HTTP_TIMEOUT)
            return response
        except requests.exceptions.RequestException:
            return None

    def _put(self, table: str, **kwargs) -> requests.Response | None:
        """
        Метод PUT-запроса.

        :param table: ``str``: рабочая таблица.

        :return: Результат запроса.
        """

        params = {"key": self.KEY}

        body = {"params": kwargs["params"], "changes": kwargs["changes"]}

        _url = f"{self.url}/{table}"

        try:
            response = requests.put(url=_url, json=body, params=params, timeout=self.HTTP_TIMEOUT)
            return response
        except requests.exceptions.RequestException:
            return None

    def light_on(self, **_) -> Response:
        """
        Метод PUT-запроса - изменения статуса устройства на ``ON``.

        :return:
        """

        OK = False
        CODES = list()

        retry = self.RETRY

        while retry > 0:
            retry -= 1

            response = self._put(
                table="Devices", params={"title": "AnLamp"}, changes={"settings": {"status": 1}}
            )

            if response is None:
                CODES.append(408)
                break

            if response.ok:
                OK = 1
                break

            CODES.append(response.status_code if response is not None else 408)

        if not OK:
            return Response(
                text=f"Не удалось выключить заданное устройство. Уточните команду и повторите попытку. \n"
                     f"Код ошибки: {CODES[-1]}",
                error=True
            )
        else:
            return Response(
                text="Устройство успешно включено."
            )

    def light_off(self, **_) -> Response:
        """
        Метод PUT-запроса - изменения статуса устройства на ``OFF``.

        :return:
        """

        OK = False
        CODES = list()

        retry = self.RETRY

        while retry > 0:
            retry -= 1

            response = self._put(
                table="Devices", params={"title": "AnLamp"}, changes={"settings": {"status": 0}}
            )

            if response is None:
                CODES.append(408)
                break

            if response.ok:
                OK = 1
                break

            CODES.append(response.status_code)

        if not OK:
            return Response(
                text=f"Не удалось выключить заданное устройство. Уточните команду и повторите попытку. \n"
                     f"Код ошибки: {CODES[-1]}",
                error=True
            )
        else:
            return Response(
                text="Устройство успешно выключено."
            )

    # TODO : implement here
    def load_settings(self):
        raise NotImplementedError

    def _post_log_command(self, log: Log) -> None:
        """
        Служебный метод `POST``-запроса - сохранение команды из лога.

        :param log: ``Log``: записываемый лог.

        :return:
        """

        OK = False
        CODES = list()

        retry = self.RETRY

        while retry > 0:
            retry -= 1

            response = self._post(
                table="Logs", raspberry_id=Environment.SELF_CODE, text=log.command.name, type="COMMAND", error=False
            )

            if response is None:
                CODES.append(408)
                break

            if response.ok:
                OK = 1
                break

            CODES.append(response.status_code)

        if not OK:
            print(f"Warning: something went wrong while posting a command (log). \n"
                  f"Retries: {self.RETRY - retry}. \n"
                  f"Status codes: {CODES}.")
        else:
            print("OK: command (log) was posted successfully.")

    def _post_log_response(self, log: Log) -> None:
        """
        Служебный метод `POST``-запроса - сохранение ответа из лога.

        :param log: ``Log``: записываемый лог.

        :return:
        """

        OK = False
        CODES = list()

        retry = self.RETRY

        while retry > 0:
            retry -= 1

            response = self._post(
                table="Logs", raspberry_id=Environment.SELF_CODE, text=log.response.get_speech(), type="RESPONSE",
                error=log.response.error
            )

            if response is None:
                CODES.append(408)
                break

            if response.ok:
                OK = 1
                break

            CODES.append(response.status_code)

        if not OK:
            print(f"Warning: something went wrong while posting a response (log). \n"
                  f"Retries: {self.RETRY - retry}. \n"
                  f"Status codes: {CODES}.")
        else:
            print("OK: response (log) was posted successfully.")

    def post_log(self, log: Log) -> None:
        """
        Метод ``POST``-запроса - сохранения лога.

        :param log: ``Log``: записываемый лог.

        :return:
        """

        self._post_log_command(log=log)
        self._post_log_response(log=log)
