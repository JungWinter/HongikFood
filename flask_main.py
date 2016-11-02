# -*- coding: utf-8 -*-
import time
from managers import APIManager, MessageManager, UserSessionManager, MenuManager
from flask import Flask, request, jsonify, session
from datetime import timedelta
from myLogger import handler, log, setLogger

app = Flask(__name__)
setLogger(app, 20)
APIAdmin = APIManager()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)


def processFail():
    message = APIAdmin.process("fail").getMessage()
    log(app, "fail")
    return jsonify(message)


@app.route("/api/failtest", methods=["GET"])
def failtest():
    return processFail(), 400


@app.route("/api/keyboard", methods=["GET"])
def yellowKeyboard():
    message = APIAdmin.process("home")
    return jsonify(message), 200


@app.route("/api/message", methods=["POST"])
def yellowMessage():
    # TODO : try-except로 에러 캐치하기

    try:
        message = APIAdmin.process("message", request.json)
        log(app, "message", request.json)
        raise
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend", methods=["POST"])
def yellowFriendAdd():
    # TODO : store user data to DB

    try:
        message = APIAdmin.process("add", request.json)
        log(app, "add", request.json)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellowFriendBlock(key):
    # TODO : delete user data to DB

    try:
        message = APIAdmin.process("block", key)
        log(app, "block", key)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def yellowExit(key):
    # TODO : expire user data to DB

    try:
        message = APIAdmin.process("exit", key)
        log(app, "exit", key)
        return jsonify(message), 200
    except:
        return processFail(), 400


if __name__ == "__main__":
    app.secret_key = 'F0Zr!8j/3y5 R~Xnn!jm?]LWX/,?RZ'
    app.run(debug=True)
