from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .myLogger import setLogger


app = Flask(__name__)
app.config.from_pyfile("config.py")
setLogger(app, 20)  # INFO Level
db = SQLAlchemy(app)

from app import views, models
