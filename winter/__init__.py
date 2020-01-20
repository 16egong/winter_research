from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from config import Config
import config

print('SQLALCHEMY_DATABASE_URI: ', Config.SQLALCHEMY_DATABASE_URI)

app = Flask(__name__)
app.config.from_object('config.Config')
socketio = SocketIO(app)
db = SQLAlchemy(app)

from winter import models

db.create_all()

if config.PHASE == 1:
    from winter import routes_phase1 as routes
elif config.PHASE == 2:
    from winter import routes_phase2 as routes
else:
    print('PHASE 1 or 2')