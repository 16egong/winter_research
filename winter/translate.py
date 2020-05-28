# Translate mandarin messages and save to db
import requests
import time, threading
import winter.models
from sqlalchemy import asc, or_, and_
from timeit import default_timer as timer
from winter import db
import logging

logger = logging.getLogger()

def translate(data):
    req = requests.get('http://mt-server:8000/' + '\"' + data.body + '\"').json()
    return req

def translate_db():
    # posts = winter.models.Posts.query.filter(winter.models.Posts.translation == None).order_by(asc(winter.models.Posts.timestamp)).all()

    posts = winter.models.Posts.query.filter(
            winter.models.Posts.translation == None,
            or_(winter.models.Posts.uid == 1, winter.models.Posts.uid == 2)) \
        .order_by(asc(winter.models.Posts.timestamp)).all()

    for data in posts:
        logging.critical('DATA TO TRANSLATE: %s UID: %s', data, data.uid)
        
        if data.uid == 1 or data.uid == 2:
                start = timer()
                req = translate(data)
                data.translation = req['translation'][1:-1]
                data.keywords =  str(','.join(req['keywords'][0:3]))
                data.translation_time = str(req['time'])
                end = timer()
                data.request_time = str(end-start)
        else:
            logger.critical('THIS SHOULD NEVER HAPPEN')
        
        data.msg_len = len(data.body)
    
        db.session.commit()

    #TODO: CHANGE THIS BACK FOR DEPLOY
    threading.Timer(10, translate_db).start() 