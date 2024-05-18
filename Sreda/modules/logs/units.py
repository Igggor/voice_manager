from Sreda.modules.text.units import Command, Response

from datetime import datetime


class Log:
    def __init__(self, command: Command, response: Response, time: datetime):
        self.command = command
        self.response = response
        self.timestamp = time
