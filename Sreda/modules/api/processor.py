from Sreda.environment import Environment

from Sreda.modules.logs.units import Log

from Sreda.static.metaclasses import SingletonMetaclass

import requests


class APIProcessor(metaclass=SingletonMetaclass):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(APIProcessor, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.url = "http://test.igreeda.keenetic.pro/api"

        self.KEY = Environment.NATIVE_API_KEY
        self.RETRY = 3

    def _get(self, **kwargs) -> requests.Response:
        """
        Метод GET-запроса.

        :return: Результат запроса или ``None`` при неудаче.
        """

        params = {"api_key": self.KEY}
        params.update(kwargs)

        response = requests.get(
            url=self.url,
            params=params
        )

        return response

    def _post(self, **kwargs) -> requests.Response:
        """
        Метод POST-запроса.

        :return: Результат запроса или ``None``.
        """

        params = {"api_key": self.KEY}

        response = requests.post(
            url=self.url,
            params=params,
            json=kwargs
        )

        return response

    def _put(self, **kwargs) -> requests.Response:
        """
        Метод PUT-запроса.

        :return: Результат запроса или ``None``.
        """

        params = {"api_key": self.KEY}

        response = requests.put(
            url=self.url,
            params=params,
            json=kwargs
        )

        return response

    # TODO : implement here
    def load_settings(self):
        pass

        # response = self._get(table="Devices", id=)

        # if not response.ok:
        #     return None
        #
        # return response.json()

    def _post_log_command(self, log: Log) -> None:
        """
        Служебный метод для POST-запроса команды из лога.

        :param log: ``Log``: записываемый лог.

        :return:
        """

        OK = False
        CODES = list()

        retry = self.RETRY

        while not OK and retry > 0:
            response = self._post(
                raspberry_id="id", text=log.command.name, type="COMMAND", error=False
            )

            if response.ok:
                OK = 1
                break

            CODES.append(response.status_code)
            retry -= 1

        if not OK:
            print(f"Warning: something went wrong while posting a command (log). \n"
                  f"Retries: {self.RETRY}. \n"
                  f"Status codes: {CODES}.")
        else:
            print("OK: command (log) was posted successfully.")

    def _post_log_response(self, log: Log) -> None:
        """
        Служебный метод для POST-запроса ответа из лога.

        :param log: ``Log``: записываемый лог.

        :return:
        """

        OK = False
        CODES = list()

        retry = self.RETRY

        while not OK and retry > 0:
            response = self._post(
                raspberry_id="id", text=log.response.get_speech(), type="RESPONSE", error=log.response.error
            )

            if response.ok:
                OK = 1
                break

            CODES.append(response.status_code)
            retry -= 1

        if not OK:
            print(f"Warning: something went wrong while posting a response (log). \n"
                  f"Retries: {self.RETRY}. \n"
                  f"Status codes: {CODES}.")
        else:
            print("OK: response (log) was posted successfully.")

    def post_log(self, log: Log) -> None:
        """
        Метод для POST-запроса лога.

        :param log: ``Log``: записываемый лог.

        :return:
        """

        self._post_log_command(log=log)
        self._post_log_response(log=log)
