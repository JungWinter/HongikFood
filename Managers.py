class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class APIManager(mataclass=Singleton):
    pass


class MessageManager(mataclass=Singleton):
    pass


class UserSessionManager(mataclass=Singleton):
    pass


class MenuManager(mataclass=Singleton):
    pass
