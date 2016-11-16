from flask import Flask
from os import path, urandom
from .myLogger import setLogger

basedir = path.abspath(path.dirname(__file__))
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TESTING=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///' + path.join(basedir, 'test.db'),
    SQLALCHEMY_ECHO=True,
    SECRET_KEY=urandom(30)
)
setLogger(app, 20)  # INFO Level

from app import views
