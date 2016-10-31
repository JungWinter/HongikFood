# -*- coding: utf-8 -*-
import time
import myLogger
from managers import APIManager, MessageManager, UserSessionManager, MenuManager
from flask import Flask, request, jsonify

app = Flask(__name__)
app.logger.addHandler(myLogger.handler)
app.logger.setLevel(20)  # INFO Level

APIAdmin = APIManager()


@app.route("/api/keyboard", methods=["GET"])
def yellowKeyboard():
    message = APIAdmin.process("home").getMessage()
    return jsonify(message), 200


@app.route("/api/message", methods=["POST"])
def yellowMessage():
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
def yellowFriendAdd():
    app.logger.info(u"[JOIN] user_key : {}".format(request.json["user_key"]))
    return jsonify(ex_success)


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellowFriendBlock(key):
    app.logger.info(u"[BLOCK] user_key : {}".format(key))
    return jsonify(ex_success)


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def yellowExit(key):
    app.logger.info(u"[EXIT] user_key : {}".format(key))
    return jsonify(ex_success)


if __name__ == "__main__":
    app.run(debug=True)
