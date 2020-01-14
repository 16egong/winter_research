import os
basedir = os.path.dirname(__file__)
# basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = 'SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False