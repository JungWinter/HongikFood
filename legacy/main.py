# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
import requestModule
import time

app = Flask(__name__)

handler = RotatingFileHandler(
    "food.log",
    maxBytes=10000000,
    backupCount=2,
    encoding="utf-8"
)
handler.setLevel(logging.INFO)
handler.setFormatter(Formatter(
    u"[%(asctime)s] %(message)s"
))
app.logger.addHandler(handler)

ex_keyboard = {
    "type": "buttons",
    "buttons": [u"오늘의 메뉴", u"내일의 메뉴", u"이번주 메뉴"]
}

ex_message = [
    {
        "message": {
            "text": u"제대로 알려주세요!\n어떤 맛있는 메뉴가 기다리고 있을까요?"
        },
        "keyboard": {
            "type": "buttons",
            "buttons": [
                u"오늘의 메뉴",
                u"내일의 메뉴",
                u"이번주 메뉴"
            ]
        }
    },
    {
        "message": {
            "text": u"=오늘의 메뉴=\n밥\n된장국\n돈까스\n뾰로롱"
        },
        "keyboard": {
            "type": "buttons",
            "buttons": [
                u"오늘의 메뉴",
                u"내일의 메뉴",
                u"이번주 메뉴"
            ]
        }
    },
    {
        "message": {
            "text": u"=내일의 메뉴=\n연어덮밥\n먹고싶다\n돈까스도\n먹고싶다"
        },
        "keyboard": {
            "type": "buttons",
            "buttons": [
                u"오늘의 메뉴",
                u"내일의 메뉴",
                u"이번주 메뉴"
            ]
        }
    },
    {
        "message": {
            "text": "여기서 확인하세요!",
            "message_button": {
                "label": "이번주 메뉴 보기",
                "url": "http://apps.hongik.ac.kr/food/food.php"
            }
        },
        "keyboard": {
            "type": "buttons",
            "buttons": [
                u"오늘의 메뉴",
                u"내일의 메뉴",
                u"이번주 메뉴"
            ]
        }
    }
]
ex_success = {
    "message": "SUCCESS"
}
ex_fail = {
    "message": "FAIL"
}

user_keys = []
keyword = [u"오늘", u"내일", u"이번주"]
admin = requestModule.Manager()
ex_message[1]["message"]["text"] = admin.getMenu()
ex_message[2]["message"]["text"] = admin.getMenu(1)


def update():
    if time.time() - admin.lastUpdate > 43200:
        admin.updateData()
        ex_message[1]["message"]["text"] = admin.getMenu()
        ex_message[2]["message"]["text"] = admin.getMenu(1)
        app.logger.info(u"[Menu Data Update]")


@app.route("/api/keyboard", methods=["GET"])
def y_keyboard():
    return jsonify(ex_keyboard)


@app.route("/api/message", methods=["POST"])
def y_message():
    app.logger.info(u"[message] user_key : {}, type : {}, content : {}".format(
        request.json["user_key"],
        request.json["type"],
        request.json["content"]))
    try:
        update()
    except:
        app.logger.error(u"[Menu Update Error]")
        return jsonify(ex_fail)
    index = 0
    try:
        for i in range(len(keyword)):
            if request.json["content"].count(keyword[i]) > 0:
                index = i+1
                break
    except:
        app.logger.error(u"[Message Error]")
        return jsonify(ex_fail)
    return jsonify(ex_message[index])


@app.route("/api/friend", methods=["POST"])
def y_friend_add():
    app.logger.info(u"[JOIN] user_key : {}".format(request.json["user_key"]))
    return jsonify(ex_success)


@app.route("/api/friend/<key>", methods=["DELETE"])
def y_friend_block(key):
    app.logger.info(u"[BLOCK] user_key : {}".format(key))
    return jsonify(ex_success)


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def y_exit(key):
    app.logger.info(u"[EXIT] user_key : {}".format(key))
    return jsonify(ex_success)


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0")
