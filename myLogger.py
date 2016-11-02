from logging.handlers import RotatingFileHandler
from logging import Formatter


handler = RotatingFileHandler(
    "HongikFood.log",
    maxBytes=1000000,
    backupCount=10,
    encoding="utf-8"
)
handler.setFormatter(Formatter(
    u"[%(asctime)s] %(message)s"
))


def setLogger(app, level):
    app.logger.addHandler(handler)
    app.logger.setLevel(level)  # INFO Level


def log(app, mode, data=None):
    '''
    app.logger.info("[JOIN] user_key : {}".format(request.json["user_key"]))
    
    app.logger.info("[BLOCK] user_key : {}".format(key))

    app.logger.info("[EXIT] user_key : {}".format(key))

    fail일때
    '''
    if mode is "message":
        app.logger.info("[message] user_key : {}, type : {}, content : {}".format(
            data["user_key"],
            data["type"],
            data["content"]))
