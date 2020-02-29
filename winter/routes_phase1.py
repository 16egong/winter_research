from flask import request, session, render_template, redirect, url_for
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


# Redirect the user to the first page they should see
@app.route('/')
def base():
    return redirect(url_for("phase_1_user_1_english_instructions"))


#PHASE1
# English
@app.route('/phase_1_user_1_english_instructions')
def phase_1_user_1_english_instructions():
    user = config.USER1
    session['uid'] = user.uid
    session['username'] = user.username
    phase_1_practice_url = url_for('phase_1_practice')
    return render_template("phase_1.0_english_instructions.html", uid=session['uid'], username=session['username'], phase_1_practice_url=phase_1_practice_url)


@app.route('/phase_1_user_2_english_instructions')
def phase_1_user_2_english_instructions():
    user = config.USER2
    session['uid'] = user.uid
    session['username'] = user.username
    phase_1_practice_url = url_for('phase_1_practice')
    return render_template("phase_1.0_english_instructions.html", uid=session['uid'], username=session['username'], phase_1_practice_url=phase_1_practice_url)


# Mandarin
@app.route('/phase_1_user_3_mandarin_instructions')
def phase_1_user_3_mandarin_instructions():
    user = config.USER3
    session['uid'] = user.uid
    session['username'] = user.username
    phase_1_practice_url = url_for('phase_1_practice')
#     return render_template("english_instructions_phase_1.html", uid=session['uid'], username=session['username'], phase_1_practice_url=phase_1_practice_url)


@app.route('/phase_1_user_4_mandarin_instructions')
def phase_1_user_4_mandarin_instructions():
    user = config.USER4
    session['uid'] = user.uid
    session['username'] = user.username
    phase_1_practice_url = url_for('phase_1_practice')
#     return render_template("english_instructions_phase_1.html", uid=session['uid'], username=session['username'], phase_1_practice_url=phase_1_practice_url)


@app.route('/phase_1_practice')
def phase_1_practice():
    uid = session.get('uid', None)
    username = session.get('username', None)
    practice_survey_url = "INSERT URL HERER"
    phase_2_english_instructions_url = url_for('phase_2_english_instructions')
    
    return render_template("phase_1.1_practice.html", username=username, practice_survey_url=practice_survey_url, phase_2_english_instructions_url=phase_2_english_instructions_url)

@app.route('/phase_2_english_instructions')
def phase_2_english_instructions():
    uid = session.get('uid', None)
    username = session.get('username', None)
    phase_2_chat_interface_url = url_for('phase_2_chat_interface')
    return render_template("phase_2.0_english_instructions.html", uid=uid, username=username, phase_2_chat_interface_url=phase_2_chat_interface_url)


@app.route('/phase_2_chat_interface', methods = ['POST', 'GET'])
def phase_2_chat_interface():
    uid = session.get('uid', None)
    username = session.get('username', None)
    usernames = config.USERNAMES

    notes = winter.models.Notes.query.filter(winter.models.Notes.uid == uid).first()
    notes = notes.notes if notes is not None else ""

    if uid == 1 or uid == 2:
        room = 'room12'
        posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 1, winter.models.Post.uid == 2)).order_by(asc(winter.models.Post.timestamp)).all()
    else:
        room = 'room34'
        posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 3, winter.models.Post.uid == 4)).order_by(asc(winter.models.Post.timestamp)).all()

    return render_template("phase_2.1_chat_interface.html", uid=uid, username=username, posts=posts, usernames=usernames, room=room, notes=notes)


@app.route('/phase_3_english_instructions')
def phase_3_english_instructions():
    uid = session.get('uid', None)
    username = session.get('username', None)
    phase_3_wait_url = url_for('phase_3_wait')
    return render_template("phase_3.0_english_instructions.html", uid=uid, username=username, phase_3_wait_url=phase_3_wait_url)


@app.route('/phase_3_wait')
def phase_3_wait():
    uid = session.get('uid', None)
    username = session.get('username', None)
    phase_3_survey_url = "INSERT URL HERER"
    phase_3_transcript_url = url_for('phase_3_transcript')
    return render_template("phase_3.10_wait.html", uid=uid, username=username, phase_3_transcript_url=phase_3_transcript_url, phase_3_survey_url=phase_3_survey_url)


@app.route('/phase_3_transcript')
def phase_3_transcript():
    uid = session.get('uid', None)
    username = session.get('username', None)
    if uid==3 or uid==4:
        posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 1, winter.models.Post.uid == 2)).order_by(asc(winter.models.Post.timestamp)).all()
    else:
        posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 3, winter.models.Post.uid == 4)).order_by(asc(winter.models.Post.timestamp)).all()
        
    phase_3_survey_url = url_for('phase_3_survey')
    return render_template("phase_3.1_transcript.html", posts=posts, phase_3_survey_url=phase_3_survey_url)


@app.route('/phase_3_survey')
def phase_3_survey():
    uid = session.get('uid', None)
    username = session.get('username', None)
    phase_4_english_instructions_url = url_for('phase_4_english_instructions')
    return render_template("phase_3.2_survey.html", uid=uid, username=username, phase_4_english_instructions_url=phase_4_english_instructions_url)
    
    
    
@app.route('/phase_4_english_instructions')
def phase_4_english_instructions():
    uid = session.get('uid', None)
    username = session.get('username', None)
    phase_3_transcript_url = url_for('phase_3_transcript')
    return render_template("phase_4.0_english_instructions.html", uid=uid, username=username, phase_4_transcript_url=phase__transcript_url)


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


@app.route("/savenotes", methods=["PUT"])
def save_notes():
    uid = request.json["uid"]
    notes = request.json["notes"]

    new_notes = winter.models.Notes(uid=uid, notes=notes)
    
    db.session.merge(new_notes)
    db.session.commit()

    return '{"success": True}', 200, {"ContentType": "application/json"}