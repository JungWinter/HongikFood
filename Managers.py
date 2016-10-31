from message import HomeMessage


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    def process(self, mode, json=None):
        if mode is "home":
            message = MessageAdmin.getHomeMessageObject()
            return message


class MessageManager(metaclass=Singleton):
    '''
    APIManager가 MessageManager한테 메시지를 요청한다.
    MessageManager는 Message와 Keyboard를 조합해 리턴한다.
    '''

    def getHomeMessageObject(self):
        homeMessage = HomeMessage()
        return homeMessage


class UserSessionManager(metaclass=Singleton):
    pass


class MenuManager(metaclass=Singleton):
    pass


MessageAdmin = MessageManager()
UserSessionAdmin = UserSessionManager()
ManuAdmin = MenuManager()

if __name__ == "__main__":
    a = APIManager()
    b = APIManager()
    assert a is b
    c = a.process("home").getMessage()
    print(c)
