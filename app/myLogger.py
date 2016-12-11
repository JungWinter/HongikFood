from logging.handlers import RotatingFileHandler
from logging import Formatter
from app import app


handler = RotatingFileHandler(
    "./app/log/HongikFood.log",
    maxBytes=10*1024*1024,
    backupCount=10,
    encoding="utf-8"
)
handler.setFormatter(Formatter(
    u"[%(asctime)s] %(message)s"
))


def setLogger(app, level):
    app.logger.addHandler(handler)
    app.logger.setLevel(level)


def customLog(msg):
    app.logger.info(msg)


def managerLog(mode, user_key):
    app.logger.info("[{}] {} {} processing completed\n".format(mode, user_key, mode))


def viewLog(mode, data=None):
    '''
    전달된 mode에 따라 로깅 내용이 달라진다.
    message : 유저키, 타입, 내용을 기록한다. json형태의 data
    add : 유저키를 기록한다. json형태의 data
    block, exit : 유저키를 기록한다. string형태의 data
    fail : 기본 request 처리 실패 로그
    '''
    if mode is "message":
        app.logger.info("[message] user_key : {}, type : {}, content : {}\n".format(
            data["user_key"],
            data["type"],
            data["content"]))
    elif mode is "add":
        app.logger.info("[join] user_key : {}\n".format(data["user_key"]))
    elif mode is "block":
        app.logger.info("[block] user_key : {}\n".format(data))
    elif mode is "exit":
        app.logger.info("[exit] user_key : {}\n".format(data))
    elif mode is "fail":
        app.logger.info("[fail] request process fail\n")
