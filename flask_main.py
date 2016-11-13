# -*- coding: utf-8 -*-
import sqlite3
from managers import APIManager, MessageManager, UserSessionManager, MenuManager
from managers import timedelta, datetime
from flask import Flask, request, jsonify, _app_ctx_stack
from myLogger import log, setLogger
from collections import defaultdict
from decorators import processtime

app = Flask(__name__)
app.secret_key = 'F1Zr!8j/3y5 R~Xnn!jm?]LWX/,?RZ'
DATABASE = "database.db"
EXPIRE_LIMIT_SECONDS = 20

setLogger(app, 20)
APIAdmin = APIManager()
userSession = defaultdict()


def getDB():
    top = _app_ctx_stack.top
    if not hasattr(top, "sqliteDB"):
        top.sqliteDB = sqlite3.connect(DATABASE)
    return top.sqliteDB


def initDB():
    with app.app_context():
        db = getDB()
        with app.open_resource("schema.sql", mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.teardown_appcontext
def closeConnection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, "sqliteDB"):
        top.sqliteDB.close()


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
    with app.app_context():
        db = getDB()
        db.cursor().execute("insert into users (user_key) values (?)", [request.json["user_key"]])
        db.commit()
    try:
        message = APIAdmin.process("add", request.json).getMessage()
        log(app, "add", request.json)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellowFriendBlock(key):
    with app.app_context():
        db = getDB()
        db.cursor().execute("delete from users where user_key = (?)", [key])
        db.commit()
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


if __name__ == "__main__":
    initDB()
    app.run(debug=True)
