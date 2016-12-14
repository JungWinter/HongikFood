from app import db, session
from datetime import timedelta, datetime
from datetime import time as createTime
from .message import BaseMessage, HomeMessage, FailMessage, SuccessMessage
from .message import SummaryMenuMessage, EvaluateMessage
from .models import User, Poll, Menu
from .menu import PlaceMenu, DayMenu
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
    def getMsgObj(self, summary, isToday, place=None, time=None):
        msgObj = MessageAdmin.getMenuMessageObject(summary, isToday, place, time)
        return msgObj

    def getCustomMsgObj(self, message):
        msgObj = MessageAdmin.getCustomMessageObject(message)
        return msgObj

    def getEvalMsgObj(self, message, step):
        msgObj = MessageAdmin.getEvaluateMessageObject(message, step)
        return msgObj

    def checkToday(self, string):
        return True if string[:2] == "오늘" else False

    def process(self, mode, data=None):
        if mode is "home":
            MenuAdmin.updateMenu()
            msgObj = MessageAdmin.getHomeMessageObject()
            return msgObj
        elif mode is "message":
            user_key = data["user_key"]
            request_type = data["type"]
            content = data["content"]
            u = User.query.filter_by(user_key=user_key).first()
            if u is None:
                u = User(user_key)
                db.session.add(u)
                db.session.commit()

            step1 = ["오늘의 식단", "내일의 식단"]
            if content in step1:
                session[user_key] = {
                    "history": [content]
                }
                summary = True
                isToday = self.checkToday(content)
                return self.getMsgObj(summary, isToday)

            step2 = ["식단 평가하기"]
            if content in step2:
                session[user_key] = {
                    "history": [content]
                }
                message = MenuAdmin.returnScore()
                return self.getEvalMsgObj(message, 1)

            step3 = ["전체 식단 보기", "학생회관", "남문관", "신기숙사", "제1기숙사", "교직원"]
            if content in step3:
                if user_key in session:
                    last = session[user_key]["history"][:]
                else:
                    last = ["오늘의 식단"]
                if last[-1] in step1:
                    summary = False
                    isToday = self.checkToday(last[-1])
                    if content == "전체 식단 보기":
                        place = None
                    else:
                        place = content
                    if user_key in session:
                        del session[user_key]
                    return self.getMsgObj(summary, isToday, place)
                elif last[-1] in step2:  # 식단평가하기에서 place를 고른상태
                    place = content
                    # 이미 user_key는 session에 있는걸 확인함
                    session[user_key]["history"].append(place)
                    message = "시간대를 골라주세요."
                    return self.getEvalMsgObj(message, 2)
                else:
                    raise

            step4 = ["아침", "점심", "저녁"]
            if content in step4:
                if user_key in session:
                    date = datetime.strftime(
                        datetime.utcnow() + timedelta(hours=9),
                        "%Y.%m.%d")
                    place = session[user_key]["history"][-1]
                    time = content
                    timelimit = {
                        "아침": createTime(hour=7, minute=20),
                        "점심": createTime(hour=10, minute=50),
                        "저녁": createTime(hour=16, minute=20),
                    }
                    u = User.query.filter_by(user_key=user_key).first()
                    m = Menu.query.filter_by(
                        date=date,
                        place=place,
                        time=time).first()
                    if m is None:  # 해당 장소에 해당 시간대가 없음
                        if user_key in session:
                            del session[user_key]
                        return self.getCustomMsgObj("{}식당에는 {}이 없습니다.".format(place, time))

                    now = datetime.utcnow() + timedelta(hours=9)
                    timenow = datetime.time(now)
                    if timenow < timelimit[time]:
                        if user_key in session:
                            del session[user_key]
                        return self.getCustomMsgObj("아직 {}시간이 아닙니다.".format(time))
                    p = Poll.query.filter_by(menu=m, user=u).first()
                    if p is None:
                        session[user_key]["history"].append(time)
                        message = "점수를 골라주세요."
                        return self.getEvalMsgObj(message, 3)
                    else:
                        if user_key in session:
                            del session[user_key]
                        return self.getCustomMsgObj("{}식당의 {}에 이미 투표하셨습니다.".format(place, time))
                else:
                    raise

            step5 = ["1", "2", "3", "4", "5"]
            if content in step5:
                if user_key in session:
                    history = session[user_key]["history"][:]
                    date = datetime.strftime(
                        datetime.utcnow() + timedelta(hours=9),
                        "%Y.%m.%d")
                    time = history[-1]
                    place = history[-2]
                    score = int(content)
                    u = User.query.filter_by(user_key=user_key).first()
                    m = Menu.query.filter_by(
                        date=date,
                        place=place,
                        time=time).first()
                    p = Poll(score, menu=m, user=u)
                    db.session.add(p)
                    db.session.commit()
                    message = "평가해주셔서 감사합니다."
                    del session[user_key]
                    return self.getEvalMsgObj(message, 4)
                else:
                    raise

            step11 = ["오늘의 점심", "오늘의 저녁", "내일의 아침"]
            if content in step11:
                if user_key in session:
                    del session[user_key]
                summary = False
                isToday = self.checkToday(content)
                place = None
                time = content[-2:]
                return self.getMsgObj(summary, isToday, place, time)

            if content == "취소":
                if user_key in session:
                    del session[user_key]
                return self.getCustomMsgObj("취소하셨습니다.")
            # 여기까지도 안걸러 졌으면 주관식 답변으로 간주

        elif mode is "add":
            user_key = data["user_key"]
            u = User(user_key)
            db.session.add(u)
            db.session.commit()

            managerLog(mode, user_key)
            msgObj = MessageAdmin.getSuccessMessageObject()
            return msgObj
        elif mode is "block":
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
        returnedMessage = BaseMessage()
        returnedMessage.updateMessage(message)
        returnedMessage.updateKeyboard(HomeMessage.returnHomeKeyboard())
        return returnedMessage

    def getMenuMessageObject(self, summary, isToday, place=None, time=None):
        message = MenuAdmin.returnMenu(isToday, summary, place, time)
        if message == "식단 정보가 없습니다.":
            return self.getCustomMessageObject(message)
        if summary:
            return SummaryMenuMessage(message, isToday)
        return self.getCustomMessageObject(message)

    def getEvaluateMessageObject(self, message, step):
        evalMessage = EvaluateMessage(message, step)
        return evalMessage

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

    def calcWday(self, isToday):
        wday = datetime.weekday(datetime.utcnow() + timedelta(hours=9))
        if not isToday:
            wday = (wday + 1) % 7
        return wday

    def checkWday(self, wday):
        return False if wday == 6 else True

    def returnMenu(self, isToday, summary=False, place=None, time=None):
        self.updateMenu()
        wday = self.calcWday(isToday)
        message = ""
        if self.checkWday(wday):
            if not place and not time:
                message = self.weekend[wday].returnAllMenu(summary)
            elif place:
                message = self.weekend[wday].returnPlaceMenu(place)
            elif time:
                message = self.weekend[wday].returnTimeMenu(time)
        else:
            message = "식단 정보가 없습니다."
        return message

    def returnScore(self):
        wday = self.calcWday(isToday=True)
        message = ""
        if self.checkWday(wday):
            message = self.weekend[wday].returnScore()
        else:
            "평가할 식단이 없습니다."
        return message


APIAdmin = APIManager()
MessageAdmin = MessageManager()
UserSessionAdmin = UserSessionManager()
MenuAdmin = MenuManager()
