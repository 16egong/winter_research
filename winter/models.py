from datetime import datetime
from winter import db

# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String)
#     real_name = db.Column(db.String)

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    username = db.Column(db.String)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    time = db.Column(db.String)

    def __repr__(self):
        return '<Post {}>'.format(self.body)