class SingletonMetaclass(type):
    __instances = {}

    def __call__(cls, **kwargs):
        if cls not in cls.__instances:
            instance = super().__call__(**kwargs)
            cls.__instances[cls] = instance
        return cls.__instances[cls]
