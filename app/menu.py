from app import db
from .models import Menu, Poll


class PlaceMenu():
    def __init__(self, place):
        self.title = None  # date + place
        self.date = None
        self.dayname = None
        self.items = {
            "아침": {
                "정보": None,
                "메뉴": [],
                "평점": None,
            },
            "점심": {
                "정보": None,
                "메뉴": [],
                "평점": None,
            },
            "저녁": {
                "정보": None,
                "메뉴": [],
                "평점": None,
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

    def returnMenu(self, summary, time=None):
        '''
        최종 메시지의 형태
        2016.11.11 금요일
        □ 남문관 (3,500원)
        ■ 점심 (11:00-15:00)
        수제탕수육
        쌀밥
        ...
        ■ 저녁 (16:30-18:30)
        제육볶음
        쌀밥
        ...
        '''
        timelist = ["아침", "점심", "저녁"]
        message = ""
        # if not time:
        #     message += "{} {}\n".format(self.date, self.dayname)
        if self.price == "":
            message += "□ {}\n".format(self.place)
        else:
            message += "□ {} ({})\n".format(self.place, self.price)

        # 메뉴 정보가 아예 없으면
        if not any([self.items[t]["메뉴"] for t in timelist]):
            message += "식단 정보가 없습니다.\n"
            return message

        for key in timelist:
            if time and key != time:
                continue
            # 메뉴가 비어있으면 건너뛰기
            if self.items[key]["메뉴"]:
                if self.items[key]["정보"] == "":
                    if self.place == "남문관" and key == "아침":
                        message += "■ 점심: 한식\n"
                    elif self.place == "남문관" and key == "점심":
                        message += "■ 점심: 양식\n"
                    else:
                        message += "■ {}\n".format(key)
                else:
                    if self.place == "남문관" and key == "아침":
                        message += "■ 점심: 한식 ({})\n".format(self.items[key]["정보"])
                    elif self.place == "남문관" and key == "점심":
                        message += "■ 점심: 양식 ({})\n".format(self.items[key]["정보"])
                    else:
                        message += "■ {} ({})\n".format(
                            key,
                            self.items[key]["정보"]
                        )
                # 평점 붙여주기
                message += "▶ " + self.items[key]["평점"] + "\n"
                # 메뉴 붙여주기
                menus = self.items[key]["메뉴"][:]
                if summary:
                    # 쌀밥 제외
                    if "쌀밥" in menus:
                        menus.remove("쌀밥")
                    message += "\n".join(menus[:4]) + "\n"
                else:
                    message += "\n".join(menus) + "\n"
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
            menu = ",".join(item)
            # m = DBAdmin.query(Menu, self.date, self.place, time[index])
            m = Menu.query.filter_by(
                date=self.date,
                place=self.place,
                time=time[index]).first()
            if not m:  # 결과값 없음
                if item:  # 빈 값이 아니면
                    # DBAdmin.addMenu(self.date, self.place, time[index], menu)
                    m = Menu(self.date, self.place, time[index], menu)
                    db.session.add(m)
                    db.session.commit()
            else:  # 결과값 있음
                if m.menu != menu:  # 비교해봐야지
                    m.menu = menu
                    # DBAdmin.commit()
                    db.session.commit()

    def updateScore(self):
        for time in self.items:
            # self.items[time]
            m = Menu.query.filter_by(
                date=self.date,
                place=self.place,
                time=time
            ).first()
            if m:  # 결과값 있음
                polls = Poll.query.filter_by(menu=m).all()
                count = len(polls)
                if count:  # 0 이상임
                    scoreSum = sum(p.score for p in polls)
                    self.items[time]["평점"] = "%.1f / 5.0" % (scoreSum / count)
                else:
                    self.items[time]["평점"] = "평가없음"


class DayMenu():
    def __init__(self, dayname):
        self.title = None  # date + dayname
        self.date = None
        self.items = [
            PlaceMenu("학생회관"),
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
            "11:30-14:00",
            "17:30-19:00",
            # 교직원 정보
            "",
            "11:30-14:20",
            "17:00-19:20",
            # 신기숙사 정보
            "7:30-9:00",
            "11:30-14:30",
            "17:30-19:20"
        ]
        time = ["아침", "점심", "저녁"]
        price = ["3,900원", "3,900원", "6,000원", "3,900원"]
        for place in self.items:
            place.price = price.pop(0)
            for t in time:
                place.items[t]["정보"] = info.pop(0)

    def returnAllMenu(self, summary):
        message = "{} {}\n".format(self.date, self.dayname)
        if summary:
            message += "> 간추린 메뉴입니다.\n"
            message += "> 쌀밥은 제외했습니다.\n"
        for place in self.items:
            message += place.returnMenu(summary=summary) + "\n"
        if summary:
            message += "\n오른쪽으로 넘기시면 다른 버튼도 있습니다.\n"
            # 특정 메시지 전달 때 여기에 추가
            # message += ""
        return message

    def returnPlaceMenu(self, place):
        '''
        search 함수도 필요할 듯
        '''
        name = ["학생회관", "남문관", "교직원", "신기숙사"]
        message = self.items[name.index(place)].returnMenu(summary=False)
        return message

    def returnTimeMenu(self, time):
        message = "{} {}\n".format(self.date, self.dayname)
        for place in self.items:
            message += place.returnMenu(summary=False, time=time) + "\n"
        return message

    def returnScore(self):
        self.updateScore()
        message = ""
        times = ["아침", "점심", "저녁"]
        for place in self.items:
            for time in times:
                if place.items[time]["메뉴"]:
                    message += "{} {} : {}\n".format(
                        place.place,
                        time,
                        place.items[time]["평점"]
                    )
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

    def updateScore(self):
        for place in self.items:
            place.updateScore()

    def update(self, date, menu):
        '''
        받은 메뉴 쪼개기
        하루에 총 10개고 4개로 나눠야함
        2 / 3 / 2 / 3
        '''
        divMenu = []
        divMenu.append([menu[0], menu[1]])
        divMenu.append([menu[2], menu[3], menu[4]])
        divMenu.append([menu[5], menu[6]])
        divMenu.append([menu[7], menu[8], menu[9]])
        if self.updateSelf(date):
            for index, item in enumerate(self.items):
                item.updateDate(date)
                item.updateMenu(divMenu[index])
                item.updateScore()
