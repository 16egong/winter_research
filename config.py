import os
import winter.users

# basedir = os.path.dirname(__file__)
basedir = os.path.abspath(os.path.dirname(__file__))

USER1 = winter.users.User(uid=1, username='Tyler', real_name='Pablo E.')
USER2 = winter.users.User(uid=2, username='Charlie', real_name='Tyrone S.')

class Config(object):
    SECRET_KEY = 'SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False