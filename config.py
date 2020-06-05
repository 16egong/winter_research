import os
from collections import defaultdict

class User:
    def __init__(self, real_name='', username='', uid=0):
        self.real_name = real_name
        self.username = username
        self.uid = uid
        
    def get_real_name(self):
        return self.real_name
    
    def get_username(self):
        return self.username
    
    def get_uid(self):
        return self.uid


# basedir = os.path.dirname(__file__)
basedir = os.path.abspath(os.path.dirname(__file__))
USERNAMES = ['Lei', 'Xiao', 'Evan', 'Joey', 'Yongle 12', 'Yongle 34']
USER1 = User(uid=1, username=USERNAMES[0])
USER2 = User(uid=2, username=USERNAMES[1])
USER3 = User(uid=3, username=USERNAMES[2])
USER4 = User(uid=4, username=USERNAMES[3])
USER12 = User(uid=12, username=USERNAMES[4])
USER34 = User(uid=34, username=USERNAMES[5])
ROOMS = defaultdict(list)

TRIAL_NUM = 2
TYPE = "keys" #switch between control, no_keys, or keys
DATABASE_NAME = f'/data/trial_{TRIAL_NUM}_' + TYPE + '.db'

class Config(object):
    SECRET_KEY = 'SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
