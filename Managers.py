from message import HomeMessage, FailMessage


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    def process(self, mode, json=None):
        if mode is "home":
            messageObj = MessageAdmin.getHomeMessageObject()
            return messageObj
        elif mode is "message":
            _user_key = json["user_key"]
            _type = json["type"]
            _content = json["content"]
            # TODO 작업중
        elif mode is "fail":
            messageObj = MessageAdmin.getFailMessageObject()
            return messageObj


class MessageManager(metaclass=Singleton):
    '''
    APIManager가 MessageManager한테 메시지를 요청한다.
    MessageManager는 Message와 Keyboard를 조합해 리턴한다.
    '''
    def getHomeMessageObject(self):
        homeMessage = HomeMessage()
        return homeMessage

    def getFailMessageObject(self):
        failMessage = FailMessage()
        return failMessage


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
    d = a.process("fail").getMessage()
    print(d)
