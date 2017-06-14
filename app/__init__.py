from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
from app import models
db.create_all()
session = defaultdict()

from app import myLogger, views
myLogger.setLogger(app, 20)
