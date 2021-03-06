from datetime import datetime
from winter import db
    
class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    username = db.Column(db.String)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    time = db.Column(db.String)
    room = db.Column(db.String)
    keywords = db.Column(db.String)
    translation = db.Column(db.String)
    translation_time = db.Column(db.String)
    request_time = db.Column(db.String)
    msg_len = db.Column(db.Integer)

    def __repr__(self):
        return '<Posts {}>'.format(self.body)

class Notes(db.Model):
    __tablename__ = "notes"

    uid = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String)

class Record(db.Model):
    __tablename__ = "record"

    uid = db.Column(db.Integer, primary_key=True)
    record = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)