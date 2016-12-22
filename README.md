# HongikFood

## 홍익대학교 학식알리미
카카오톡 옐로아이디(@홍익대학교학식알리미)를 통해
홍익대학교 학식의 구성을 간편하게 확인할 수 있는 챗봇서비스입니다.

## 기반
- Python3 + flask + SQLAlchemy
- ubuntu 14.04 + nginx + uwsgi
- Kakaotalk YellowID

## 개요
```
user request
      |
      v
Flask main app -> APIManager <-> UserSessionManager
                      ^       <-> DBManager
                      |
                  MessageManager <- Message <- MenuManager <- Requester
```

### 파일 별 역할
- `config.py` - Flask와 SQLAlchemy설정
- `keyboard.py` - 응답 버튼 구현체
- `message.py` - 추상화된 `Message` 클래스와 구현체 선언
- `managers.py` - 실질적 데이터 처리 부분
  - `APIManager` - REST API 구분 및 `view`에 응답객체 반환
  - `MessageManager` - 적절한 `Message`와 `Keyboard`를 조합해 전달
  - `MenuManager` - 맥락에 따라 적절한 `Menu Message`를 전달
  - `UserSessionManager` - 전역 유저 세션 담당
  - `DBManager` - 전역 DB 질의 담당
- `models.py` - SQLAlchemy 스키마 선언
- `views.py` - Flask 구현체, Kakaotalk yellowid API 명세에 따름
- `menu.py` - `Menu` 클래스 선언, `Menu Message` 생성

## 챗봇 응답 목록
```
공통 - [요약된 식단 표시] - 전체 식단 보기
                          학생회관
                          남문관
                          신기숙사
                          교직원
오늘의 식단 - 오늘의 점심
             오늘의 저녁
내일의 식단 - 내일의 아침
식단 평가하기 - 학생회관 - 점심 - 1, 2, 3, 4, 5
                         저녁
               남문관
               신기숙사
               교직원
```

### 로그 분석 - 2016.12.22 기준
#### 이용횟수 Top5 유저
![user request top10](https://github.com/JungWinter/HongikFood/blob/master/app/static/img/users_limit.png?raw=true)

#### 요청 Top5 날짜
![date top5](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/date_top5.png)

#### 요청 Bottom5 날짜
![date bottom5](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/date_bottom5.png)

#### 업데이트 이전
![all messages](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/messages_before_update.png)

#### 업데이트 이후 (2016년 12월 10일~)
![message after update](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/messages_after_update.png)

#### 2016 하반기
![message after update](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/2016.png)

#### 월별
![message after update](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/month.png)

#### 2016 11월
![message after update](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/2016-11.png)

#### 2016년 12월 12일 (최다 이용 날짜)
![message after update](https://raw.githubusercontent.com/JungWinter/HongikFood/master/app/static/img/2016-12-12.png)
