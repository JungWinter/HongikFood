# -*- coding: utf-8 -*-
from app import app
from flask import request, jsonify
import traceback
from .managers import APIAdmin
from .myLogger import viewLog


def processFail():
    message = APIAdmin.process("fail").getMessage()
    viewLog("fail")
    return jsonify(message)


@app.route("/api/keyboard", methods=["GET"])
def yellowKeyboard():
    message = APIAdmin.process("home").getMessage()
    return jsonify(message), 200


@app.route("/api/message", methods=["POST"])
def yellowMessage():
    try:
        viewLog("message", request.json)
        message = APIAdmin.process("message", request.json).getMessage()
        return jsonify(message), 200
    except:
        traceback.print_exc()
        return processFail(), 400


@app.route("/api/friend", methods=["POST"])
def yellowFriendAdd():
    try:
        viewLog("add", request.json)
        message = APIAdmin.process("add", request.json).getMessage()
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellowFriendBlock(key):
    try:
        viewLog("block", key)
        message = APIAdmin.process("block", key).getMessage()
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def yellowExit(key):
    try:
        viewLog("exit", key)
        message = APIAdmin.process("exit", key).getMessage()
        return jsonify(message), 200
    except:
        return processFail(), 400
