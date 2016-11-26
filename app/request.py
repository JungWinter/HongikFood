# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

def tagTostr(tag):
    return tag.get_text().strip()

def getSoup():
    pass

def updateDateAndMenu():
    pass

def updateAll():
    r = requests.get("http://apps.hongik.ac.kr/food/food.php")
    soup = BeautifulSoup(r.text, "lxml")

    thead = tagTostr(soup.find("thead"))
    head = thead.split()[1:]
    key = [w[:3] for w in head]  # 월요일, 화요일, ...
    value = [w[4:-1] for w in head]  # 2016.11.21, 2016.11.22, ...
    dates = list(zip(wday, value))

    subtitles = [tagTostr(i) for i in soup.find_all("tr", class_="subtitle")]
    '''
    subtitle은 학생회관 남문관은 장소 / 시간등의 정보
    그 외는 그냥 장소 로만 되어있음
    example :
        학생회관식당 / 11:00~14:00(점심), 17:00~19:00(저녁) (토요일 휴업)
        남문관식당(제2식당) /  11:00~15:00(점심), 16:30~18:30(저녁) (토요일 휴업)
        교직원식당
    Menu클래스에게 던져주면 알아서 판단하게끔
    '''

    menus = [tagTostr(i) for i in soup.find_all("div", class_="daily-menu")]
    '''
    월 : 0, 6, 12 ..., 화 : 1, 7, 13 ...
    menus는 횡적으로 구성되어있음.
    월요일에 대한 학생회관 점심, 저녁 / 남문관 점심 , 저녁 이렇게가 아니라
    월화수목금토에 대한 학생회관 점심, 월화수목금토에 대한 학생회관 저녁 이렇게
    총 54개 (하루에 9개 * 6일)
    6개씩 건너뛰며 횡적 배열을 종적 배열로 바꿔줘야함
    '''
