import os
import winter.users

# basedir = os.path.dirname(__file__)
basedir = os.path.abspath(os.path.dirname(__file__))
USERNAMES = ['Lei', 'Xiao', 'Evan', 'Joey', 'Yongle 12', 'Yongle 34']
USER1 = winter.users.User(uid=1, username=USERNAMES[0])
USER2 = winter.users.User(uid=2, username=USERNAMES[1])
USER3 = winter.users.User(uid=3, username=USERNAMES[2])
USER4 = winter.users.User(uid=4, username=USERNAMES[3])
USER12 = winter.users.User(uid=12, username=USERNAMES[4])
USER34 = winter.users.User(uid=34, username=USERNAMES[5])

TRIAL_NUM = 1
TYPE = "control" #switch between control, no_keys, or keys
DATABASE_NAME = f'/data/trial_{TRIAL_NUM}_' + TYPE + '.db'


class Config(object):
    SECRET_KEY = 'SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
