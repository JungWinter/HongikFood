from app import db, session
from .message import HomeMessage, FailMessage, SuccessMessage
from .models import User, Poll
from .myLogger import managerLog


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    # lastUpdate = datetime.now()

    def process(self, mode, data=None):
        if mode is "home":
            messageObj = MessageAdmin.getHomeMessageObject()
            return messageObj
        elif mode is "message":
            '''
            타입체크 -> content체크 -> 세션체크 -> 명령처리
            '''
            _user_key = data["user_key"]
            _type = data["type"]
            _content = data["content"]
        elif mode is "add":
            '''
            새로운 유저 등록
            '''
            user_key = data["user_key"]
            u = User(user_key)
            db.session.add(u)
            db.session.commit()
            messageObj = MessageAdmin.getSuccessMessageObject()
            return messageObj
        elif mode is "block":
            '''
            기존 유저 삭제
            '''
            user_key = data
            if session.get(user_key) is not None:
                session.pop(user_key)
            u = User.query.filter_by(user_key=user_key).first()
            db.session.delete(u)
            db.session.commit()
            managerLog(mode, user_key)

            messageObj = MessageAdmin.getSuccessMessageObject()
            return messageObj
        elif mode is "exit":
            '''
            세션 정보 삭제
            '''
            user_key = data
            if session.get(user_key) is not None:
                session.pop(user_key)
            managerLog(mode, user_key)

            messageObj = MessageAdmin.getSuccessMessageObject()
            return messageObj
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
        return successMessage


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
