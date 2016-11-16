# -*- coding: utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup


class Weekend():
    def __init__(self, text):
        self.day = text
        self.date = ""
        self.data = {
            u"학관": {
                u"점심": "",
                u"저녁": ""
            },
            u"남문관": {
                u"점심": "",
                u"저녁": ""
            },
            u"교직원": {
                u"점심": "",
                u"저녁": ""
            },
            u"신기숙사": {
                u"아침": "",
                u"점심": "",
                u"저녁": ""
            }
        }
# 접근 : mon.data["학관"]["점심"]


class Manager():
    def __init__(self):
        mon = Weekend(u"월요일")
        tue = Weekend(u"화요일")
        wen = Weekend(u"수요일")
        thu = Weekend(u"목요일")
        fri = Weekend(u"금요일")
        sat = Weekend(u"토요일")
        self.weekends = [mon, tue, wen, thu, fri, sat]
        self.titles = []
        self.setDate()
        self.setMenu()
        self.lastUpdate = time.time()

    def getHtml(self):
        r = requests.get("http://apps.hongik.ac.kr/food/food.php")
        # path = './temp/response1.html'
        # with open(path, 'rb') as testfile:
        #     r = testfile.read()
        # with open(path,'wb') as testfile:
        #     testfile.write(r.content)
        soup = BeautifulSoup(r.content, "html.parser")
        # soup = BeautifulSoup(r, "lxml")
        return soup

    def getDate(self):
        soup = self.getHtml()
        check_string = str(soup.find("thead"))
        check_string = "".join(check_string.split('\n'))
        pattern = re.compile(r"([가-힣]{3}).+?(\d{4}[.]\d{2}[.]\d{2})")
        result = pattern.findall(check_string)  # tuple in list
        return result

    def setDate(self):
        result = self.getDate()
        for i in range(len(self.weekends)):
            self.weekends[i].date = result[i][1]

    def setMenu(self):
        soup = self.getHtml()
        for word in soup.find_all("tr", class_="subtitle"):
            self.titles.append(word.get_text().lstrip().rstrip())
        count = 0
        for word in soup.find_all("div", class_="daily-menu"):
            menu = word.get_text().lstrip().rstrip()
            if count < 6:
                self.weekends[count].data[u"학관"][u"점심"] = menu
            elif count < 12:
                self.weekends[count % 6].data[u"학관"][u"저녁"] = menu
            elif count < 18:
                self.weekends[count % 6].data[u"남문관"][u"점심"] = menu
            elif count < 24:
                self.weekends[count % 6].data[u"남문관"][u"저녁"] = menu
            elif count < 30:
                self.weekends[count % 6].data[u"교직원"][u"점심"] = menu
            elif count < 36:
                self.weekends[count % 6].data[u"교직원"][u"저녁"] = menu
            elif count < 42:
                self.weekends[count % 6].data[u"신기숙사"][u"아침"] = menu
            elif count < 48:
                self.weekends[count % 6].data[u"신기숙사"][u"점심"] = menu
            elif count < 54:
                self.weekends[count % 6].data[u"신기숙사"][u"저녁"] = menu
            count += 1
        # print(soup.find("div",class_="daily-menu").get_text())

    def getMenu(self, mode=0):
        # mode : 0 = today, 1 = tomorrow
        wday = time.localtime()[6]  # wday : 0 = monday
        message = ""
        if (mode == 0 and wday == 6) or (mode == 1 and wday == 5):
            message = u"메뉴 정보가 없습니다"
            return message
        if mode == 1:
            wday = (wday + 1) % 7

        message = ""
        message += self.weekends[wday].date + " " + self.weekends[wday].day + "\n\n"
        message += "<<" + self.titles[0] + ">>\n"
        message += u"===점심 (3,900원)===\n"
        message += self.weekends[wday].data[u"학관"][u"점심"] + "\n\n"
        message += u"===저녁 (3,900원)===\n"
        message += self.weekends[wday].data[u"학관"][u"저녁"] + "\n\n"
        # message += u"===옛향 (저녁)===\n"
        # message += self.weekends[wday].data[u"학관"][u"저녁"] + "\n\n"
        message += "<<" + self.titles[1] + ">>\n"
        message += u"===점심 (3,500원)===\n"
        message += self.weekends[wday].data[u"남문관"][u"점심"] + "\n\n"
        message += u"===저녁 (3,500원)===\n"
        message += self.weekends[wday].data[u"남문관"][u"저녁"] + "\n\n"
        message += "<<" + self.titles[2] + ">>\n"
        message += u"===점심===\n"
        message += self.weekends[wday].data[u"교직원"][u"점심"] + "\n\n"
        message += u"===저녁===\n"
        message += self.weekends[wday].data[u"교직원"][u"저녁"] + "\n\n"
        message += "<<" + self.titles[3] + ">>\n"
        message += u"===아침 (7:30~9:00)===\n"
        message += self.weekends[wday].data[u"신기숙사"][u"아침"] + "\n\n"
        message += u"===점심 (11:30~14:30)===\n"
        message += self.weekends[wday].data[u"신기숙사"][u"점심"] + "\n\n"
        message += u"===저녁 (17:30~19:30)===\n"
        message += self.weekends[wday].data[u"신기숙사"][u"저녁"] + "\n\n"

        return message

    def updateData(self):
        self.dataReset()
        self.setDate()
        self.setMenu()
        self.lastUpdate = time.time()

    def dataReset(self):
        self.date = ""
        self.data = {
            u"학관": {
                u"점심": "",
                u"저녁": ""
            },
            u"남문관": {
                u"점심": "",
                u"저녁": ""
            },
            u"교직원": {
                u"점심": "",
                u"저녁": ""
            },
            u"신기숙사": {
                u"아침": "",
                u"점심": "",
                u"저녁": ""
            }
        }

if __name__ == "__main__":
    admin = Manager()
    print(admin.getMenu(1))
