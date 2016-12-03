from app import db
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(32), index=True, unique=True)
    join_date = db.Column(db.DateTime)
    last_active_date = db.Column(db.DateTime)

    def __init__(self, user_key):
        self.user_key = user_key
        self.join_date = datetime.utcnow() + timedelta(hours=9)
        self.last_active_date = self.join_date

    def __repr__(self):
        return "<User %r>" % (self.user_key)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    place = db.Column(db.String())
    time = db.Column(db.String())
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("polls", lazy="dynamic"))

    def __init__(self, place, time, score, user):
        self.place = place
        self.time = time
        self.score = score
        self.user = user
        self.timestamp = datetime.utcnow() + timedelta(hours=9)

    def __repr__(self):
        return "<Poll %r>" % (self.place+"-"+self.time+"-"+str(self.score))


class PlaceMenu():
    def __init__(self, place):
        self.title = None  # date + place
        self.date = None
        self.dayname = None
        self.items = {
            "아침": {
                "정보": None,
                "메뉴": [],
            },
            "점심": {
                "정보": None,
                "메뉴": [],
            },
            "저녁": {
                "정보": None,
                "메뉴": [],
            },
        }
        self.place = place

    def test(self):
        print("%s PlaceMenu TEST" % self.place)
        print("title : %s" % self.title)
        print("dayname : %s" % self.dayname)
        print("date : %s" % self.date)
        print("아침 정보 : %s" % self.items["아침"]["정보"])
        print("점심 정보 : %s" % self.items["점심"]["정보"])
        print("저녁 정보 : %s" % self.items["저녁"]["정보"])
        print("아침 : %s" % " ".join(self.items["아침"]["메뉴"]))
        print("점심 : %s" % " ".join(self.items["점심"]["메뉴"]))
        print("저녁 : %s" % " ".join(self.items["저녁"]["메뉴"]))

    def summarize(self):
        message = ""
        message += "<<" + self.place + ">>\n"
        for item in itmes:  # item is dict type
            k = list(item)[0]  # use only first element
            v = item[k]
            message += "===" + k + "===\n"
            for line in v.split()[:4]:
                message += line.strip() + "\n"
            message += "\n"
        return message

    def updateDate(self, date):
        self.dayname = date[0]
        self.date = date[1]

    def updateMenu(self, menu):
        '''
        menu의 길이가 2면 아침없음
        3이면 아침있음
        '''
        time = ["저녁", "점심", "아침"]
        reverseMenu = list(reversed(menu))
        for index, item in enumerate(reverseMenu):
            self.items[time[index]]["메뉴"] = item


class DayMenu():
    def __init__(self, dayname):
        self.title = None  # date + dayname
        self.date = None
        self.items = [
            PlaceMenu("학관"),
            PlaceMenu("남문관"),
            PlaceMenu("교직원"),
            PlaceMenu("신기숙사"),
            # PlaceMenu("제1기숙사"),
        ]
        self.dayname = dayname

        info = [
            # 학관 정보
            "",
            "11:00-14:00\n3,900원",
            "17:00-19:00\n3,900원",
            # 남문관 정보
            "",
            "11:00-15:00\n3,500원",
            "16:30-18:30\n3,500원",
            # 교직원 정보
            "",
            "6,000원",
            "6,000원",
            # 신기숙사 정보
            "7:30-9:00",
            "11:30-14:30",
            "17:30-19:30"
        ]
        time = ["아침", "점심", "저녁"]
        for place in self.items:
            for t in time:
                place.items[t]["정보"] = info.pop(0)

    def updateSelf(self, date):
        '''
        아마 맞겠지만 그래도 검증
        '''
        if self.dayname == date[0]:
            self.date = date[1]
            return True
        else:
            return False

    def update(self, date, menu):
        '''
        받은 메뉴 쪼개기
        하루에 총 9개고 4개로 나눠야함
        2 / 2 / 2 / 3
        '''
        divMenu = []
        divMenu.append([menu[0], menu[1]])
        divMenu.append([menu[2], menu[3]])
        divMenu.append([menu[4], menu[5]])
        divMenu.append([menu[6], menu[7], menu[8]])
        if self.updateSelf(date):
            for index, item in enumerate(self.items):
                item.updateDate(date)
                item.updateMenu(divMenu[index])
            for item in self.items:
                print("============================")
                print(self.dayname, self.date)
                item.test()
        else:
            print("삐빅")
