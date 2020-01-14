from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from config import Config

print('SQLALCHEMY_DATABASE_URI: ', Config.SQLALCHEMY_DATABASE_URI)

app = Flask(__name__)
app.config.from_object('config.Config')
socketio = SocketIO(app)
db = SQLAlchemy(app)

from winter import models

db.create_all()

from winter import routes