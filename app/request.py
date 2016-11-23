# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup


def step01():
    '''
    레거시 코드 걷어내고 구조화 안한 상태
    크게 구분하면
        soup객체 얻어오기
        re검사로 wday와 date 얻어오기 -> 동적
        subtitle로 장소 / 정보 얻어오기 -> 정적
        menu로 식단 얻어오기 -> 동적
    '''
    r = requests.get("http://apps.hongik.ac.kr/food/food.php")
    soup = BeautifulSoup(r.text, "lxml")

    head = str(soup.find("thead"))
    head = "".join(head.split("\n"))
    pattern = re.compile(r"([가-힣]{3}).+?(\d{4}[.]\d{2}[.]\d{2})")
    result = pattern.findall(head)  # [("월요일", "2016.11.21"), ...]
    for k, v in result:
        pass
        '''
        k는 wday (월요일-토요일)
        v는 2016.11.21형식의 date
        Menu클래스에게 던져주기
        '''

    subtitles = soup.find_all("tr", class_="subtitle")
    for item in subtitles:
        subtitle = item.get_text().strip()
        '''
        subtitle은 학생회관 남문관은 장소 / 시간등의 정보
        그 외는 그냥 장소 로만 되어있음
        example :
            학생회관식당 / 11:00~14:00(점심), 17:00~19:00(저녁) (토요일 휴업)
            남문관식당(제2식당) /  11:00~15:00(점심), 16:30~18:30(저녁) (토요일 휴업)
            교직원식당
        Menu클래스에게 던져주면 알아서 판단하게끔
        '''

    menus = soup.find_all("div", class_="daily-menu")
    for item in menus:
        menuList = item.get_text().split()
        '''
        menus는 횡적으로 구성되어있음.
        월요일에 대한 학생회관 점심, 저녁 / 남문관 점심 , 저녁 이렇게가 아니라
        월화수목금토에 대한 학생회관 점심, 월화수목금토에 대한 학생회관 저녁 이렇게
        총 54개 (하루에 9개 * 6일)
        6개씩 건너뛰며 횡적 배열을 종적 배열로 바꿔줘야함
        '''
