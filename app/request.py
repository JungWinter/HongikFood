import requests
from bs4 import BeautifulSoup

soup = None


def _tagTostr(tag):
    return tag.get_text().strip()


def _getSoup():
    r = requests.get("http://apps.hongik.ac.kr/food/food.php")
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def _soupToDates(soup):
    try:
        thead = _tagTostr(soup.find("thead"))
        head = thead.split()[1:]
    except AttributeError:
        head = ["로딩중(0000.00.00)"] * 6
    key = [w[:3] for w in head]  # 월요일, 화요일, ...
    value = [w[4:-1] for w in head]  # 2016.11.21, 2016.11.22, ...
    dates = list(zip(key, value))
    return dates


def _soupToMenus(soup):
    '''
    월 : 0, 6, 12 ..., 화 : 1, 7, 13 ...
    menus는 횡적으로 구성되어있음.
    월요일에 대한 학생회관 점심, 저녁 / 남문관 점심 , 저녁 이렇게가 아니라
    월화수목금토에 대한 학생회관 점심, 월화수목금토에 대한 학생회관 저녁 이렇게
    총 54개 (하루에 9개 * 6일)
    6개씩 건너뛰며 횡적 배열을 종적 배열로 바꿔줘야함
    '''
    cols = []
    menus = [_tagTostr(i).split() for i in soup.find_all("div", class_="daily-menu")]
    for item in menus:
        if item and item[0] in ["[중식]", "[석식]"]:
            del item[0]
    if menus == []:
        cols = [["-"] * 10] * 6
    if len(menus) == 54:
        transmenus = [list(menu) for menu in zip(*[iter(menus)]*6)]
        rows = [iter(i) for i in transmenus]
        cols = [list(col) for col in zip(*rows)]
    if len(menus) == 60:
        transmenus = [list(menu) for menu in zip(*[iter(menus)]*6)]
        rows = [iter(i) for i in transmenus]
        cols = [list(col) for col in zip(*rows)]
    return cols


def _soupToSubtitles(soup):
    '''
    subtitle은 학생회관 남문관은 장소 / 시간등의 정보
    그 외는 그냥 장소 로만 되어있음
    example :
        학생회관식당 / 11:00~14:00(점심), 17:00~19:00(저녁) (토요일 휴업)
        남문관식당(제2식당) /  11:00~15:00(점심), 16:30~18:30(저녁) (토요일 휴업)
        교직원식당
    Menu클래스에게 던져주면 알아서 판단하게끔
    '''
    subtitles = [_tagTostr(i) for i in soup.find_all("tr", class_="subtitle")]
    return subtitles


def getDatesAndMenus():
    '''
    dates와 menus를 반환함
    menus는 2차원 리스트
    dates는 튜플이 들어있는 리스트
    '''
    soup = _getSoup()
    dates = _soupToDates(soup)
    menus = _soupToMenus(soup)
    return dates, menus
