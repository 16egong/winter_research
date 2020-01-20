import os
import winter.users

# basedir = os.path.dirname(__file__)
basedir = os.path.abspath(os.path.dirname(__file__))
USERNAMES = ['Tyler', 'Charlie', 'Sam', 'Jamie']
USER1 = winter.users.User(uid=1, username=USERNAMES[0])
USER2 = winter.users.User(uid=2, username=USERNAMES[1])
USER3 = winter.users.User(uid=3, username=USERNAMES[2])
USER4 = winter.users.User(uid=4, username=USERNAMES[3])

PHASE = 1
DATABASE_NAME = 'trial_1' + str(PHASE)


class Config(object):
    SECRET_KEY = 'SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False