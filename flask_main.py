# -*- coding: utf-8 -*-
from managers import APIManager, MessageManager, UserSessionManager, MenuManager
from managers import timedelta, datetime
from flask import Flask, request, jsonify
from myLogger import log, setLogger
from collections import defaultdict

app = Flask(__name__)
# app.permanent_session_lifetime = timedelta(seconds=20)
setLogger(app, 20)

EXPIRE_LIMIT_SECONDS = 20
APIAdmin = APIManager()
session = defaultdict()

@app.route("/api/failtest", methods=["GET"])
def failtest():
    return processFail(), 400


@app.route("/api/session", methods=["GET"])
def sessiontest():
    print(session)
    return str(session), 200


@app.route("/api/session/<value>", methods=["GET"])
def sessioninputtest(value):
    now = datetime.utcnow() + timedelta(hours=9)
    now = int(now.timestamp())
    session[value] = {
        "time": now
    }
    print(session)
    return str(session), 200


def sessionCheck():
    now = datetime.utcnow() + timedelta(hours=9)
    now = now.timestamp()

    # type 1
    expireList = []
    for key in session:
        if now - session[key]["time"] > EXPIRE_LIMIT_SECONDS:
            expireList.append(item)
    for item in expireList:
        session.pop(item, None)

    # type 2
    for key in session.keys():
        if now - session[key]["time"] > EXPIRE_LIMIT_SECONDS:
            del session[key]


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
    # TODO : store user data to DB

    try:
        message = APIAdmin.process("add", request.json).getMessage()
        log(app, "add", request.json)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellowFriendBlock(key):
    # TODO : delete user data to DB

    try:
        message = APIAdmin.process("block", key).getMessage()
        log(app, "block", key)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def yellowExit(key):
    # TODO : expire user data to DB

    try:
        message = APIAdmin.process("exit", key).getMessage()
        log(app, "exit", key)
        return jsonify(message), 200
    except:
        return processFail(), 400


if __name__ == "__main__":
    app.secret_key = 'F1Zr!8j/3y5 R~Xnn!jm?]LWX/,?RZ'
    app.run(debug=True)
