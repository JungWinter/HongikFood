from message import Message
from keyboard import Keyboard


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    @staticmethod
    def getHomeMessage():
        return MessageAdmin.getHomeMessage()


class MessageManager(metaclass=Singleton):
    '''
    APIManager가 MessageManager한테 메시지를 요청한다.
    MessageManager는 Message와 Keyboard를 조합해 리턴한다.
    '''
    @staticmethod
    def getHomeMessage():
        homeKeyboard = Keyboard.homeButtons
        homeMessage = Message.ex_keyboard
        homeMessage["buttons"] = homeKeyboard
        return homeMessage


class UserSessionManager(metaclass=Singleton):
    pass


class MenuManager(metaclass=Singleton):
    pass

APIAdmin = APIManager()
MessageAdmin = MessageManager()
UserSessionAdmin = UserSessionManager()
ManuAdmin = MenuManager()

if __name__ == "__main__":
    a = APIManager()
    b = APIManager()
    assert a is b
