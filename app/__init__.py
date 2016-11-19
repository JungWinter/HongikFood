from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict


app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
session = defaultdict()

from app import views, models, myLogger

myLogger.setLogger(app, 20)
