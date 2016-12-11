from app import db
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(32), index=True, unique=True)
    join_date = db.Column(db.String())
    last_active_date = db.Column(db.String())

    def __init__(self, user_key):
        self.user_key = user_key
        self.join_date = datetime.strftime(
            datetime.utcnow() + timedelta(hours=9),
            "%Y.%m.%d %H:%M:%S")
        self.last_active_date = self.join_date

    def __repr__(self):
        return "<User %r>" % (self.user_key)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    score = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    menu = db.relationship("Menu", backref=db.backref("polls", lazy="dynamic"))
    user = db.relationship("User", backref=db.backref("polls", lazy="dynamic"))

    def __init__(self, score, menu, user):
        self.score = score
        self.menu = menu
        self.user = user
        self.date = datetime.strftime(
            datetime.utcnow() + timedelta(hours=9),
            "%Y.%m.%d")

    def __repr__(self):
        return "<Poll %r>" % (self.user.user_key+"-"+str(self.score))


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    place = db.Column(db.String())
    time = db.Column(db.String())
    menu = db.Column(db.String())

    def __init__(self, date, place, time, menu):
        self.date = date
        self.place = place
        self.time = time
        self.menu = menu

    def __repr__(self):
        return "<Menu %r>" % (self.date+"-"+self.place+"-"+self.time)
