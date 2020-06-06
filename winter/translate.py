# Translate mandarin messages and save to db
import requests
import time, threading
import winter.models
from sqlalchemy import asc, or_, and_
from timeit import default_timer as timer
from winter import db
import logging

logger = logging.getLogger()

def get_keywords(data):
    logging.critical('REQUESTING KEYWORDS FOR: %s', data.body)
    req = requests.get('http://mt-server:8000/keywords', params={"sentence": data.body}).json()
    logging.critical('KEYWORD RESULTS: %s', req)
    return req


def get_translation(data):
    logging.critical('REQUESTING TRANSLATION FOR: %s', data.body)
    req = requests.get('http://mt-server:8000/translate', params={"sentence": data.body}).json()
    logging.critical('TRANSLATION RESULTS: %s', req)
    return req

def translate_db():
    # posts = winter.models.Posts.query.filter(winter.models.Posts.translation == None).order_by(asc(winter.models.Posts.timestamp)).all()

    posts = winter.models.Posts.query.filter(
            winter.models.Posts.translation == None) \
        .order_by(asc(winter.models.Posts.timestamp)).all()

    for data in posts:
        if data.uid == 1 or data.uid == 2:
            logging.critical('DATA TO TRANSLATE: %s UID: %s', data, data.uid)
            start = timer()
            req = get_translation(data)
            data.translation = req['translation']
            data.keywords =  str(','.join(req['keywords'][0:3]))
            data.translation_time = str(req['time'])
            end = timer()
            data.request_time = str(end-start)
        else:
            logging.critical('KEYWORDS: %s ', data.keywords)
            start = timer()
            req = get_keywords(data)
            data.translation = data.body
            data.keywords =  str(','.join(req['keywords'][0:3]))
            data.translation_time = str(req['time'])
            end = timer()
            data.request_time = str(end-start)
        
        data.msg_len = len(data.body)
    
        db.session.commit()

    #TODO: CHANGE THIS BACK FOR DEPLOY
    threading.Timer(10, translate_db).start() 