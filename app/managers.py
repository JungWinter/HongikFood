from app import db, session
from datetime import timedelta, datetime
from .message import BaseMessage, HomeMessage, FailMessage, SuccessMessage
from .message import SummaryMenuMessage
from .models import User, Poll, PlaceMenu, DayMenu
from .myLogger import managerLog, customLog
from .request import getDatesAndMenus
from .decorators import processtime


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):

    def process(self, mode, data=None):
        if mode is "home":
            MenuAdmin.updateMenu()
            msgObj = MessageAdmin.getHomeMessageObject()
            return msgObj
        elif mode is "message":
            user_key = data["user_key"]
            request_type = data["type"]
            content = data["content"]

            step1 = ["오늘의 식단", "내일의 식단"]
            step2 = ["식단 평가하기"]
            step3 = ["전체 식단 보기", "학생회관", "남문관", "신기숙사", "제1기숙사", "교직원"]
            step4 = ["아침", "점심", "저녁"]
            step5 = ["1", "2", "3", "4", "5"]
            step11 = ["오늘의 점심", "오늘의 저녁", "내일의 아침"]

            if content in step1:
                now = datetime.utcnow() + timedelta(hours=9)
                now = int(now.timestamp())
                session[user_key] = {
                    "time": now,
                    "history": [content]
                }
                if content == "오늘의 식단":
                    isToday = True
                elif content == "내일의 식단":
                    isToday = False
                msgObj = MessageAdmin.getMenuMessageObject(True, isToday)
                return msgObj
            elif content in step2:
                msgObj = MessageAdmin.getCustomMessageObject("개발중입니다.")
                return msgObj
            elif content in step3:
                '''
                세션에서 history를 가져옴 -> 만약 없으면 Fail처리
                그래서 식단 평가하기 문맥인지 오늘/내일의 식단 문맥인지 확인
                그거에 따라 isToday변수 활성화
                메시지 반환전에 세션에서 삭제
                '''
                if user_key in session:
                    last = session[user_key]["history"][:]
                    del session[user_key]
                else:
                    last = ["오늘의 식단"]
                if last[-1] in step1:
                    if last[-1] == "오늘의 식단":
                        isToday = True
                    elif last[-1] == "내일의 식단":
                        isToday = False

                    if content == "전체 식단 보기":
                        msgObj = MessageAdmin.getMenuMessageObject(False, isToday)
                        return msgObj
                    else:
                        msgObj = MessageAdmin.getMenuMessageObject(False, isToday, content)
                        return msgObj

            elif content in step4:
                pass
            elif content in step5:
                '''
                평가를 DB에 기록
                '''
                if user_key in session:
                    del session[user_key]
            elif content in step6:
                if user_key in session:
                    del session[user_key]
            elif content == "취소":
                if user_key in session:
                    del session[user_key]
                msgObj = MessageAdmin.getCustomMessageObject("취소하셨습니다.")
                return msgObj
        elif mode is "add":
            '''
            새로운 유저 등록
            '''
            user_key = data["user_key"]
            u = User(user_key)
            db.session.add(u)
            db.session.commit()

            managerLog(mode, user_key)
            msgObj = MessageAdmin.getSuccessMessageObject()
            return msgObj
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
            msgObj = MessageAdmin.getSuccessMessageObject()
            return msgObj
        elif mode is "exit":
            '''
            유효성 검사
            세션 정보 삭제
            '''
            user_key = data
            if session.get(user_key) is not None:
                session.pop(user_key)

            managerLog(mode, user_key)
            msgObj = MessageAdmin.getSuccessMessageObject()
            return msgObj
        elif mode is "fail":
            msgObj = MessageAdmin.getFailMessageObject()
            return msgObj


class MessageManager(metaclass=Singleton):
    '''
    APIManager가 MessageManager한테 메시지를 요청한다.
    MessageManager는 Message와 Keyboard를 조합해 리턴한다.
    '''
    def getCustomMessageObject(self, message):
        _message = BaseMessage()
        _message.updateMessage(message)
        _message.updateKeyboard(HomeMessage.returnHomeKeyboard())
        return _message

    def getMenuMessageObject(self, summary, isToday, place=None):
        if not place:
            message = MenuAdmin.returnEveryWhereMenu(summary, isToday)
            if summary:
                summaryMessage = SummaryMenuMessage(message, isToday)
                return summaryMessage
            else:
                wholeMessage = self.getCustomMessageObject(message)
                return wholeMessage
        else:
            message = MenuAdmin.returnSpecificMenu(isToday, place)
            placeMessage = self.getCustomMessageObject(message)
            return placeMessage

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
        self.lastUpdateTime = 0
        self.updateMenu()

    def updateMenu(self):
        now = int(datetime.timestamp(datetime.utcnow() + timedelta(hours=9)))
        # timedelta.total_seconds(timedelta(hours=1)) 로 비교해도 되는데 느릴까봐
        if now - self.lastUpdateTime > 3600:
            self.lastUpdateTime = now
            dates, menus = getDatesAndMenus()
            for index, day in enumerate(self.weekend):
                day.update(date=dates[index], menu=menus[index])

    def returnEveryWhereMenu(self, summary, isToday):
        self.updateMenu()
        wday = datetime.weekday(datetime.utcnow() + timedelta(hours=9))
        if not isToday:
            wday = (wday + 1) % 7
        message = self.weekend[wday-1].returnAllMenu(summary)
        return message

    def returnSpecificMenu(self, isToday, place):
        wday = datetime.weekday(datetime.utcnow() + timedelta(hours=9))
        if not isToday:
            wday = (wday + 1) % 7
        message = self.weekend[wday-1].returnPlaceMenu(place)
        return message

    def returnDinner(self):
        pass

    def returnLunch(self):
        pass


APIAdmin = APIManager()
MessageAdmin = MessageManager()
UserSessionAdmin = UserSessionManager()
MenuAdmin = MenuManager()
