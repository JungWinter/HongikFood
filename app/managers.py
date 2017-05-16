from app import db, session
from datetime import timedelta, datetime
from datetime import time as createTime
from .message import BaseMessage, HomeMessage, FailMessage, SuccessMessage
from .message import SummaryMenuMessage, EvaluateMessage
from .models import User, Poll, Menu
from .menu import DayMenu
from .request import getDatesAndMenus
from .myLogger import managerLog


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

    def checkWhole(self, string):
        return True if string[:2] == "전체" else False

    def process(self, mode, data=None):
        if mode is "home":
            msgObj = MessageAdmin.getHomeMessageObject()
            return msgObj
        elif mode is "message":
            MenuAdmin.updateMenu()
            user_key = data["user_key"]
            request_type = data["type"]
            content = data["content"]
            DBAdmin.updateUserActionDate(user_key)

            step1 = ["오늘의 식단", "내일의 식단", "오늘의 메뉴", "내일의 메뉴"]
            if content in step1:
                UserSessionAdmin.init(user_key, content)
                summary = True
                isToday = self.checkToday(content)
                return self.getMsgObj(summary, isToday)

            step2 = ["식단 평가하기"]
            if content in step2:
                UserSessionAdmin.init(user_key, content)
                message = MenuAdmin.returnScore()
                message += "\n주관식 평가는 준비중입니다.\n실제로 먹어본 식단만 평가해주세요!"
                return self.getEvalMsgObj(message, 1)

            step3 = ["전체 식단 보기", "학생회관", "남문관", "신기숙사", "제1기숙사", "교직원"]
            if content in step3:
                last = UserSessionAdmin.getHistory(user_key)
                if last[-1] in step1:
                    summary = False
                    isToday = self.checkToday(last[-1])
                    place = None if self.checkWhole(content) else content
                    UserSessionAdmin.delete(user_key)
                    return self.getMsgObj(summary, isToday, place)
                elif last[-1] in step2:  # 식단평가하기에서 place를 고른상태
                    place = content
                    UserSessionAdmin.addHistory(user_key, place)
                    message = "시간대를 골라주세요."
                    return self.getEvalMsgObj(message, 2)
                else:
                    raise

            step4 = ["아침", "점심", "저녁"]
            if content in step4:
                if UserSessionAdmin.checkExist(user_key):
                    now = datetime.utcnow() + timedelta(hours=9)
                    date = datetime.strftime(now, "%Y.%m.%d")
                    place = UserSessionAdmin.getHistory(user_key).pop()
                    time = content
                    timenow = datetime.time(now)
                    if timenow < MenuAdmin.timelimit[time]:
                        UserSessionAdmin.delete(user_key)
                        return self.getCustomMsgObj("아직 {}시간이 아닙니다.".format(time))

                    u = DBAdmin.query(User, user_key)
                    m = DBAdmin.query(Menu, date, place, time)
                    if m is None:  # 해당 장소에 해당 시간대가 없음
                        UserSessionAdmin.delete(user_key)
                        return self.getCustomMsgObj("{}식당에는 {}이 없습니다.".format(place, time))

                    p = DBAdmin.query(Poll, m, u)
                    if p:
                        UserSessionAdmin.delete(user_key)
                        return self.getCustomMsgObj("{}식당의 {}에 이미 투표하셨습니다.".format(place, time))
                    UserSessionAdmin.addHistory(user_key, time)
                    message = "점수를 골라주세요."
                    return self.getEvalMsgObj(message, 3)
                else:
                    DBAdmin.addUser(user_key)
                    UserSessionAdmin.init(user_key, content)
                    managerLog(mode, user_key)
                    self.process(mode, data)

            step5 = ["1", "2", "3", "4", "5"]
            if content in step5:
                if UserSessionAdmin.checkExist(user_key):
                    now = datetime.utcnow() + timedelta(hours=9)
                    history = UserSessionAdmin.getHistory(user_key)
                    date = datetime.strftime(now, "%Y.%m.%d")
                    time = history[-1]
                    place = history[-2]
                    score = int(content)
                    u = DBAdmin.query(User, user_key)
                    m = DBAdmin.query(Menu, date, place, time)
                    DBAdmin.addPoll(score, m, u)
                    message = "평가해주셔서 감사합니다."
                    UserSessionAdmin.delete(user_key)
                    return self.getEvalMsgObj(message, 4)
                else:
                    DBAdmin.addUser(user_key)
                    UserSessionAdmin.init(user_key, content)
                    managerLog(mode, user_key)
                    self.process(mode, data)

            step11 = ["오늘의 점심", "오늘의 저녁", "내일의 아침"]
            if content in step11:
                summary = False
                isToday = self.checkToday(content)
                place = None
                time = content[-2:]
                UserSessionAdmin.delete(user_key)
                return self.getMsgObj(summary, isToday, place, time)

            if content == "취소":
                UserSessionAdmin.delete(user_key)
                return self.getCustomMsgObj("취소하셨습니다.")
            # 여기까지도 안걸러 졌으면 주관식 답변으로 간주

        elif mode is "add":
            user_key = data["user_key"]
            DBAdmin.addUser(user_key)
            managerLog(mode, user_key)
            msgObj = MessageAdmin.getSuccessMessageObject()
            return msgObj
        elif mode is "block":
            user_key = data
            UserSessionAdmin.delete(user_key)
            DBAdmin.deleteUser(user_key)
            managerLog(mode, user_key)
            msgObj = MessageAdmin.getSuccessMessageObject()
            return msgObj
        elif mode is "exit":
            user_key = data
            UserSessionAdmin.delete(user_key)
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

        if message[:12] == "식단 정보가 없습니다.":
            # returnedMessage.add_photo(url, width, height)
            pass
        return returnedMessage

    def getMenuMessageObject(self, summary, isToday, place=None, time=None):
        message = MenuAdmin.returnMenu(isToday, summary, place, time)
        if message == "식단 정보가 없습니다.":
            # 특성 메시지 전달 때 이곳에
            # message += "..." 으로 추가
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
    def checkExist(self, user_key):
        return True if user_key in session else False

    def init(self, user_key, content):
        session[user_key] = {
            "history": [content]
        }

    def delete(self, user_key):
        if self.checkExist(user_key):
            del user_key

    def addHistory(self, user_key, action):
        if self.checkExist(user_key):
            session[user_key]["history"].append(action)

    def getHistory(self, user_key):
        if self.checkExist(user_key):
            return session[user_key]["history"][:]
        else:
            return ["오늘의 식단"]


class DBManager(metaclass=Singleton):
    def query(self, model, *args):
        if model == User:
            user_key = args[0]
            return User.query.filter_by(user_key=user_key).first()
        elif model == Menu:
            if len(args) == 3:
                date = args[0]
                place = args[1]
                time = args[2]
                return Menu.query.filter_by(date=date, place=place, time=time).first()
        elif model == Poll:
            if len(args) == 2:
                menu = args[0]
                user = args[1]
                return Poll.query.filter_by(menu=menu, user=user).first()

    def updateUserActionDate(self, user_key):
        u = self.query(User, user_key)
        if u:
            u.last_active_date = datetime.strftime(
                datetime.utcnow() + timedelta(hours=9),
                "%Y.%m.%d %H:%M:%S")
            self.commit()
        else:
            self.addUser(user_key)

    def addUser(self, user_key):
        u = self.query(User, user_key)
        if u is None:
            u = User(user_key)
            self.add(u)

    def deleteUser(self, user_key):
        u = self.query(User, user_key)
        if u is not None:
            self.delete(u)

    def addPoll(self, score, menu, user):
        p = Poll(score, menu=menu, user=user)
        self.add(p)

    def addMenu(self, date, place, time, menu):
        m = Menu(date, place, time, menu)
        self.add(m)

    def delete(self, obj):
        db.session.delete(obj)
        self.commit()

    def add(self, obj):
        db.session.add(obj)
        self.commit()

    def commit(self):
        db.session.commit()


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
        self.timelimit = {
            "아침": createTime(hour=7, minute=20),
            "점심": createTime(hour=10, minute=50),
            "저녁": createTime(hour=16, minute=20),
        }
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
        self.updateScore()
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
        self.updateScore()
        wday = self.calcWday(isToday=True)
        message = ""
        if self.checkWday(wday):
            message = self.weekend[wday].returnScore()
        else:
            "평가할 식단이 없습니다."
        return message

    def updateScore(self):
        wday = self.calcWday(isToday=True)
        if self.checkWday(wday):
            self.weekend[wday].updateScore()


APIAdmin = APIManager()
MessageAdmin = MessageManager()
UserSessionAdmin = UserSessionManager()
MenuAdmin = MenuManager()
DBAdmin = DBManager()
