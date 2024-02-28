# Класс глобальных настроек.
# Singleton - pattern
class GlobalContext:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GlobalContext, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.ON = False
