# -*- coding: utf-8 -*-
from app import app, db
from flask import request, jsonify
from collections import defaultdict
from datetime import timedelta, datetime
from .managers import APIManager, MessageManager, UserSessionManager, MenuManager
from .myLogger import log
from .decorators import processtime


EXPIRE_LIMIT_SECONDS = 20

APIAdmin = APIManager()
userSession = defaultdict()


@app.route("/api/failtest", methods=["GET"])
def failtest():
    return processFail(), 400


@app.route("/api/session", methods=["GET"])
def sessiontest():
    print(userSession)
    return str(userSession), 200


@app.route("/api/session/<value>", methods=["GET"])
def sessioninputtest(value):
    now = datetime.utcnow() + timedelta(hours=9)
    now = int(now.timestamp())
    userSession[value] = {
        "time": now,
        "act": "test",
    }
    print(userSession)
    return str(userSession), 200


@processtime
def sessionCheck():
    now = datetime.utcnow() + timedelta(hours=9)
    now = now.timestamp()

    for key in list(userSession):
        if now - userSession[key]["time"] > EXPIRE_LIMIT_SECONDS:
            del userSession[key]


def processFail():
    message = APIAdmin.process("fail").getMessage()
    log(app, "fail")
    return jsonify(message)


@app.route("/api/keyboard", methods=["GET"])
def yellowKeyboard():
    message = APIAdmin.process("home").getMessage()
    return jsonify(message), 200


@app.route("/api/message", methods=["POST"])
def yellowMessage():
    # TODO : try-except로 에러 캐치하기

    try:
        message = APIAdmin.process("message", request.json).getMessage()
        log(app, "message", request.json)
        raise
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend", methods=["POST"])
def yellowFriendAdd():
    try:
        message = APIAdmin.process("add", request.json).getMessage()
        log(app, "add", request.json)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellowFriendBlock(key):
    try:
        message = APIAdmin.process("block", key).getMessage()
        log(app, "block", key)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def yellowExit(key):
    # TODO : expire user session

    try:
        message = APIAdmin.process("exit", key).getMessage()
        log(app, "exit", key)
        return jsonify(message), 200
    except:
        return processFail(), 400
