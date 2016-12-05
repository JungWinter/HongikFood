from app import db, session
from datetime import timedelta, datetime
from .message import HomeMessage, FailMessage, SuccessMessage
from .models import User, Poll, PlaceMenu, DayMenu
from .myLogger import managerLog
from .request import getDatesAndMenus


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
            MenuAdmin.updateMenu()
            messageObj = MessageAdmin.getHomeMessageObject()
            return messageObj
        elif mode is "message":
            '''
            메뉴 업데이트 -> 타입체크 -> content체크 -> 세션체크 -> 명령처리
            '''
            user_key = data["user_key"]
            request_type = data["type"]
            content = data["content"]

            '''
            step1에 속하면 session에 유저 키를 등록
            step2에 속하면 그 전 문맥이 무엇이었는지 파악 필요
            step2에 속하고 식단 평가가 아니면 세션 만료
            step3에 속하면 place정보 파악 필요
            step4에 속하면 place, when정보 파악 필요, 세션 만료
            '''
            step1 = ["오늘의 식단", "내일의 식단", "식단 평가하기"]
            step2 = ["전체 식단 보기", "학생회관", "남문관", "신기숙사", "제1기숙사", "교직원"]
            step3 = ["아침", "점심", "저녁"]
            step4 = ["1", "2", "3", "4", "5"]
            step5 = ["오늘의 점심", "오늘의 저녁", "내일의 아침"]

            if content in step1:
                now = datetime.utcnow() + timedelta(hours=9)
                now = int(now.timestamp())
                session[user_key] = {
                    "time": now,
                    "history": [content]
                }
            elif content in step2:
                pass
            elif content in step3:
                pass
            elif content in step4:
                '''
                평가를 DB에 기록
                '''
                if user_key in session:
                    del session[user_key]
            elif content in step5:

                if user_key in session:
                    del session[user_key]
            elif content == "취소":
                if user_key in session:
                    del session[user_key]
                # 메시지와 함께 홈키 반환
        elif mode is "add":
            '''
            새로운 유저 등록
            '''
            user_key = data["user_key"]
            u = User(user_key)
            db.session.add(u)
            db.session.commit()

            managerLog(mode, user_key)
            messageObj = MessageAdmin.getSuccessMessageObject()
            return messageObj
        elif mode is "block":
            '''
            유효성 검사
            기존 유저 삭제
            '''
            user_key = data
            if session.get(user_key) is not None:
                session.pop(user_key)
            u = User.query.filter_by(user_key=user_key).first()
            if u is not None:
                db.session.delete(u)
                db.session.commit()

            managerLog(mode, user_key)
            messageObj = MessageAdmin.getSuccessMessageObject()
            return messageObj
        elif mode is "exit":
            '''
            유효성 검사
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
    '''
    Testcase:
        오늘의 학생식당 식단
        내일의 남문관 식단
        오늘의 점심
        내일의 전체메뉴 보기
    '''
    def __init__(self):
        mon = DayMenu("월요일")
        tue = DayMenu("화요일")
        wed = DayMenu("수요일")
        thu = DayMenu("목요일")
        fri = DayMenu("금요일")
        sat = DayMenu("토요일")
        self.weekend = [mon, tue, wed, thu, fri, sat]

    def updateMenu(self):
        dates, menus = getDatesAndMenus()
        for index, day in enumerate(self.weekend):
            day.update(date=dates[index], menu=menus[index])

    def returnTodayMenu(self):
        pass

    def returnTomorrowMenu(self):
        pass

    def returnLunch(self):
        pass


APIAdmin = APIManager()
MessageAdmin = MessageManager()
UserSessionAdmin = UserSessionManager()
MenuAdmin = MenuManager()
