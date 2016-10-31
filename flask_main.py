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
    # TODO : try-except로 에러 캐치하기
    #        logging분리하기
    app.logger.info("[message] user_key : {}, type : {}, content : {}".format(
        request.json["user_key"],
        request.json["type"],
        request.json["content"]))
    message = APIAdmin.process("message", request.json).getMessage()
    return jsonify(message), 200


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
    app.secret_key = 'F0Zr!8j/3y5 R~Xnn!jm?]LWX/,?RZ'
    app.run(debug=True)
