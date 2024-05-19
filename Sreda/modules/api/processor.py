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
        self.url = "http://haha.com"

        self.KEY = Environment.NATIVE_API_KEY

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
        params.update(kwargs)

        response = requests.post(
            url=self.url,
            params=params
        )

        return response

    def _put(self, **kwargs) -> requests.Response:
        """
        Метод PUT-запроса.

        :return: Результат запроса или ``None``.
        """

        params = {"api_key": self.KEY}
        params.update(kwargs)

        response = requests.put(
            url=self.url,
            params=params
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

    def post_log(self, log: Log):
        pass
