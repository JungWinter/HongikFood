from message import HomeMessage, FailMessage, SuccessMessage
from datetime import datetime, timedelta


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    lastUpdate = datetime.now()

    def process(self, mode, data=None):
        if mode is "home":
            messageObj = MessageAdmin.getHomeMessageObject()
            return messageObj
        elif mode is "message":
            _user_key = data["user_key"]
            _type = data["type"]
            _content = data["content"]
        elif mode is "add":
            messageObj = MessageAdmin.getSuccessMessageObject()
            return messageObj
        elif mode is "block":
            pass
        elif mode is "exit":
            pass
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

    def getSuccessMessageObject(self):
        successMessage = SuccessMessage()
        return SuccessMessage


class UserSessionManager(metaclass=Singleton):
    def add(self):
        pass

    def blcok(self):
        pass

    def exit(self):
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
    d = a.process("fail").getMessage()
