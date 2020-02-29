from flask import session, render_template, url_for
from flask_socketio import emit, send, join_room, leave_room
from winter import app
from winter import socketio
from winter import db
import winter.models
import winter.users
from sqlalchemy import asc, or_
import pandas as pd
import config
import time
from datetime import datetime
import pytz
import requests

# db = SQLAlchemy(app)

def fake_call(url_link):
    return {
        "time": "0.83 secs",
        "keywords": ["word1", "w2", "keyword3"],
        "translation": "The 28-year-old cook was found dead at a shopping mall in San Francisco"}

#PHASE1
# English
@app.route('/english_instructions_1_1')
def e_inst_phase1_user1():
    user = config.USER1
    session['uid'] = user.uid
    session['username'] = user.username
    practice_page_url = url_for('practice_phase_1')
    return render_template("english_instructions_phase_1.html", uid=session['uid'], username=session['username'], practice_page_url=practice_page_url)

@app.route('/english_instructions_1_2')
def e_inst_phase1_user2():
    user = config.USER2
    session['uid'] = user.uid
    session['username'] = user.username
    practice_page_url = url_for('practice_phase_1')
    return render_template("english_instructions_phase_1.html", uid=session['uid'], username=session['username'], practice_page_url=practice_page_url)

# Mandarin
@app.route('/mandarin_instructions_1_3')
def m_inst_phase1_user3():
    user = config.USER3
    session['uid'] = user.uid
    session['username'] = user.username
    practice_page_url = url_for('practice_phase_1')
    return render_template("english_instructions_phase_1.html", uid=session['uid'], username=session['username'], practice_page_url=practice_page_url)

@app.route('/mandarin_instructions_1_4')
def m_inst_phase1_user4():
    user = config.USER4
    session['uid'] = user.uid
    session['username'] = user.username
    practice_page_url = url_for('practice_phase_1')
    return render_template("english_instructions_phase_1.html", uid=session['uid'], username=session['username'], practice_page_url=practice_page_url)

@app.route('/practice_1')
def practice_phase_1():
    uid = session.get('uid', None)
    username = session.get('username', None)
    practice_survey_url = "INSERT URL HERER"
    english_phase_2_instructions_url = url_for('e_inst_phase_2')
    
    return render_template("practice.html", username=username, practice_survey_url=practice_survey_url, english_phase_2_instructions_url=english_phase_2_instructions_url)

@app.route('/english_instructions_2')
def e_inst_phase_2():
    uid = session.get('uid', None)
    username = session.get('username', None)
    chat_interface_url = url_for('chat_interface_2')
    return render_template("english_instructions_phase_2.html", uid=uid, username=username, chat_interface_url=chat_interface_url)


@app.route('/chat_interface_2', methods = ['POST', 'GET'])
def chat_interface_2():
    uid = session.get('uid', None)
    username = session.get('username', None)
    usernames = config.USERNAMES
    if uid == 1 or uid == 2:
        room = 'room12'
        posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 1, winter.models.Post.uid == 2)).order_by(asc(winter.models.Post.timestamp)).all()
    else:
        room = 'room34'
        posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 3, winter.models.Post.uid == 4)).order_by(asc(winter.models.Post.timestamp)).all()
        
    return render_template("chat_phase_2.html", uid=uid, username=username, posts=posts, usernames=usernames, room=room)

@app.route('/1')
def inst1():
    user = config.USER1
    chat_url = url_for('chat1')
    cv_url = url_for('cv_p1')
    return render_template("instructions_1.html", uid=user.uid, chat_url=chat_url, cv_url=cv_url)


@app.route('/2')
def inst2():
    user = config.USER2
    chat_url = url_for('chat2')
    cv_url = url_for('cv_p2')
    return render_template("instructions_1.html", uid=user.uid, chat_url=chat_url, cv_url=cv_url)


@app.route('/inst_p3')
def inst3():
    user = config.USER3
    chat_url = url_for('chat3')
    cv_url = url_for('cv_p3')
    return render_template("instructions_1.html", uid=user.uid, chat_url=chat_url, cv_url=cv_url)


@app.route('/4')
def inst4():
    user = config.USER4
    chat_url = url_for('chat4')
    cv_url = url_for('cv_p4')
    return render_template("instructions_1.html", uid=user.uid, chat_url=chat_url, cv_url=cv_url)
    
@app.route('/cv_p1')
def cv_p1():
    user = config.USER1
    return render_template("cv.html", username=user.username, uid=user.uid)


@app.route('/cv_p2')
def cv_p2():
    user = config.USER2
    return render_template("cv.html", username=user.username, uid=user.uid)


@app.route('/cv_p3')
def cv_p3():
    user = config.USER3
    return render_template("cv.html", username=user.username, uid=user.uid)


@app.route('/cv_p4')
def cv_p4():
    user = config.USER4
    return render_template("cv.html", username=user.username, uid=user.uid)

    
@app.route('/chat1',methods = ['POST', 'GET'])
def chat1():
    room = 'room12'
    user = config.USER1
    posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 1, winter.models.Post.uid == 2)).order_by(asc(winter.models.Post.timestamp)).all()
    usernames = config.USERNAMES
    
            
    return render_template("chat.html", uid=user.uid, username=user.username, posts=posts, usernames=usernames, room=room)


@app.route('/chat2',methods = ['POST', 'GET'])
def chat2():
    room = 'room12'
    user = config.USER2
    posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 1, winter.models.Post.uid == 2)).order_by(asc(winter.models.Post.timestamp)).all()
    usernames = config.USERNAMES
            
    return render_template("chat.html", uid=user.uid, username=user.username, posts=posts, usernames=usernames, room=room)


@app.route('/chat3',methods = ['POST', 'GET'])
def chat3():
    room = 'room34'
    user = config.USER3
    posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 3, winter.models.Post.uid == 4)).order_by(asc(winter.models.Post.timestamp)).all()
    usernames = config.USERNAMES
            
    return render_template("chat.html", uid=user.uid, username=user.username, posts=posts,  usernames=usernames, room=room)


@app.route('/chat4',methods = ['POST', 'GET'])
def chat4():
    room = 'room34'
    user = config.USER4
    posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 3, winter.models.Post.uid == 4)).order_by(asc(winter.models.Post.timestamp)).all()
    usernames = config.USERNAMES
            
    return render_template("chat.html", uid=user.uid, username=user.username, posts=posts,  usernames=usernames, room=room)


@app.route('/transcript')
def transcript_12():
    posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 1, winter.models.Post.uid == 2)).order_by(asc(winter.models.Post.timestamp)).all()
    string_chinese= "这位28岁的厨师在旧金山一家购物中心被发现死亡"
    fake_link = ('http://10.104.101.60:8009/'+string_chinese)
    fake_call(fake_link)
    print('TEST POST: ', test_post.text)
    test_post=test_post.text
    return render_template("transcript.html", posts=posts, test_post=test_post)


@app.route('/transcript_34')
def transcript_34():
    posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 3, winter.models.Post.uid == 4)).order_by(asc(winter.models.Post.timestamp)).all()
    return render_template("transcript.html", posts=posts)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
#     send({'msg': username + ' has entered the room.'}, room=room)
    emit('join_room', {'msg': username + ' has entered the room.'}, room=room)
    
    
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('message')
def message(data):
    try:
        print('MESSAGE')
        
        tz = pytz.timezone('US/Eastern')
        data['time'] = str(datetime.now(tz).strftime('%I:%M %p'))
        
        post = winter.models.Post(uid=data['uid'], username= data['username'], 
                                  body=data['msg'], time=data['time'])
        db.session.add(post)
        db.session.commit()
        
        print(f'\n\n{data}\n\n')

        # gets sent to the message bucket on client side
        room = data['room']
        send(data, room=room)
    except Exception as e:
        print('ELSE: ', e )
        print(f'\n\n{data}\n\n')
        send(data, broadcast=True)

@socketio.on('typing')
def typing(data):
    emit('display', data, room=data['room'], include_self=True)
# if __name__ == '__main__':
#     socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')
    # socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')