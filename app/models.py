from app import db
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(32), index=True, unique=True)
    join_date = db.Column(db.DateTime)
    last_active_date = db.Column(db.DateTime)

    def __init__(self, user_key):
        self.user_key = user_key
        self.join_date = datetime.utcnow() + timedelta(hours=9)
        self.last_active_date = self.join_date

    def __repr__(self):
        return "<User %r>" % (self.user_key)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    place = db.Column(db.String())
    time = db.Column(db.String())
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("polls", lazy="dynamic"))

    def __init__(self, place, time, score, user):
        self.place = place
        self.time = time
        self.score = score
        self.user = user
        self.timestamp = datetime.utcnow() + timedelta(hours=9)

    def __repr__(self):
        return "<Poll %r>" % (self.place+"-"+self.time+"-"+str(self.score))
