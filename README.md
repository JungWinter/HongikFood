# HongikFood

## 홍익대학교 학식알리미
카카오톡 옐로아이디(@홍익대학교학식알리미)를 통해
홍익대학교 학식의 구성을 간편하게 확인할 수 있는 서비스입니다.

## Basis
- Python flask
- ubuntu 14.04 (My own server)
- nginx + uwsgi
- kakaotalk yellowid auto_reply

## Overview
@ TODO : UML로 만든 이미지 적용
```
user request
      |
      v
Flask main app -> APIManager <- UserSessionManager <- DepthChecker
                      ^
                      |
                  MessageManager <- Message <- keyboard
                                            <- menu <- Requester
                                                    <- Parser
                                                    -> Database
```

## Flow
```
오늘의 식단 - [요약된 식단 표시] - 전체 식단 보기
                                 학생회관
                                 남문관
                                 신기숙사
                                 제1기숙사
                                 교직원
내일의 식단 - 위와 같음
이번주 식단 - [학교 홈페이지의 식단표 링크]
식단 평가하기 - 학생회관 - 1, 2, 3, 4, 5
               남문관
               신기숙사
               제1기숙사
               교직원
```

## TODO
- [ ] Flask route -> Class 테스트
- [ ] 서버에서 python3로 돌리기
- [x] user_id 고유값 확인
  - 고유함
- [x] Message클래스 구성하기
- [x] User Session 관리기능 만들기
- [ ] SessionCheck 효율 높이기
- [ ] DB모델 만들기
- [ ] 비동기IO 적용하기
- [ ] Flask-RESTful 적용하기
- [ ] Flask-SQLAlchemy 적용하기
- [x] 식단 갱신시간 변경하기
- [ ] 제1기숙사 식단 적용하기
- [x] Log구성 바꾸기
- [ ] Log기록 분석
  - [ ] 일별 사용량 추이
  - [ ] 오늘/내일/이번주 요청 횟수 추이
  - [ ] 사용자 분석
- [ ] 라이브서버 외에서 테스트 하기
- [ ] requirements.txt 만들기
