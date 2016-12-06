from app import db
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(32), index=True, unique=True)
    join_date = db.Column(db.String())
    last_active_date = db.Column(db.String())

    def __init__(self, user_key):
        self.user_key = user_key
        self.join_date = datetime.strftime(
            datetime.utcnow() + timedelta(hours=9),
            "%Y.%m.%d %H:%M:%S")
        self.last_active_date = self.join_date

    def __repr__(self):
        return "<User %r>" % (self.user_key)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    score = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    menu = db.relationship("Menu", backref=db.backref("polls", lazy="dynamic"))
    user = db.relationship("User", backref=db.backref("polls", lazy="dynamic"))

    def __init__(self, score, menu, user):
        self.score = score
        self.menu = menu
        self.user = user
        self.date = datetime.strftime(
            datetime.utcnow() + timedelta(hours=9),
            "%Y.%m.%d")

    def __repr__(self):
        return "<Poll %r>" % (self.user.user_key+"-"+str(self.score))


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    place = db.Column(db.String())
    time = db.Column(db.String())
    menu = db.Column(db.String())

    def __init__(self, date, place, time, menu):
        self.date = date
        self.place = place
        self.time = time
        self.menu = menu

    def __repr__(self):
        return "<Menu %r>" % (self.date+"-"+self.place+"-"+self.time)


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
        self.price = None

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

    def returnMenu(self, summary):
        '''
        최종 메시지의 형태
        2016.11.11 금요일
        ■ 남문관 (3,500원)
        □ 점심 (11:00-15:00)
        수제탕수육
        쌀밥
        ...
        □ 저녁 (16:30-18:30)
        제육볶음
        쌀밥
        ...
        '''
        time = ["아침", "점심", "저녁"]
        message = ""
        message += "{} {}\n".format(self.date, self.dayname)
        if self.price == "":
            message += "□ {}\n".format(self.place)
        else:
            message += "□ {} ({})\n".format(self.place, self.price)

        # 메뉴 정보가 아예 없으면
        if not any([self.items[t]["메뉴"] for t in time]):
            message += "식단 정보가 없습니다.\n"
            return message

        for key in time:
            # 메뉴가 비어있으면 건너뛰기
            if self.items[key]["메뉴"]:
                if self.items[key]["정보"] == "":
                    message += "■ {}\n".format(key)
                else:
                    message += "■ {} ({})\n".format(
                        key,
                        self.items[key]["정보"]
                    )
                # for menu in self.items[key]["메뉴"]:
                #     message += "{:_>18}\n".format(menu)
                # 메뉴 붙여주기
                if summary:
                    # 쌀밥 제외
                    menus = self.items[key]["메뉴"][:]
                    if "쌀밥" in menus:
                        menus.remove("쌀밥")
                    message += "\n".join(menus[:4]) + "\n"
                else:
                    message += "\n".join(self.items[key]["메뉴"]) + "\n"

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
            "11:00-14:00",
            "17:00-19:00",
            # 남문관 정보
            "",
            "11:00-15:00",
            "16:30-18:30",
            # 교직원 정보
            "",
            "",
            "",
            # 신기숙사 정보
            "7:30-9:00",
            "11:30-14:30",
            "17:30-19:30"
        ]
        time = ["아침", "점심", "저녁"]
        price = ["3,900원", "3,500원", "6,000원", ""]
        for place in self.items:
            place.price = price.pop(0)
            for t in time:
                place.items[t]["정보"] = info.pop(0)

    def returnAllMenu(self, summary):
        message = ""
        for place in self.items:
            message += place.returnMenu(summary=summary) + "\n"
        return message

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
