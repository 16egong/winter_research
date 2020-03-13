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


# # Redirect the user to the first page they should see
# @app.route('/')
# def base():
#     return redirect(url_for("phase_1_user_1_english_instructions"))
@app.route('/<int:uid>')
def base(uid):
    session["uid"] = uid

    return redirect(url_for("control", phase=1, subphase=0))

users = [config.USER1, config.USER2, config.USER3, config.USER4]

def get_sitemap():
    """ A bit of a hack to get this dictionary to be properly populated """
    if get_sitemap.sitemap is None:
        get_sitemap.sitemap = {
            "1.0": {
                "type": "user_specific_instructions",
                "user1": url_for("static", filename="docs/phase_1.0_user_1_CN_instructions.pdf"),
                "user2": url_for("static", filename="docs/phase_1.0_user_2_CN_instructions.pdf"),
                "user3": url_for("static", filename="docs/phase_1.0_user_3_EN_instructions.pdf"),
                "user4": url_for("static", filename="docs/phase_1.0_user_4_EN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=1),
            },
            "1.1": {
                "type": "instructions",
                "english": url_for("static", filename="docs/phase_1.1_EN_instructions.pdf"),
                "mandarin": url_for("static", filename="docs/phase_1.1_CN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=2),
            },
            "1.2": {
                "type": "user_specific_instructions",
                "user1": url_for("static", filename="docs/phase_1.2_user_1_CN_instructions.pdf"),
                "user2": url_for("static", filename="docs/phase_1.2_user_2_CN_instructions.pdf"),
                "user3": url_for("static", filename="docs/phase_1.2_user_3_EN_instructions.pdf"),
                "user4": url_for("static", filename="docs/phase_1.2_user_4_EN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=3),
            },
            "1.3": {
                "type": "instructions",
                "english": url_for("static", filename="docs/phase_1.3_EN_instructions.pdf"),
                "mandarin": url_for("static", filename="docs/phase_1.3_CN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=4),
            },
            "1.4": {
                "type": "instructions",
                "english": url_for("static", filename="docs/phase_1.4_EN_instructions.pdf"),
                "mandarin": url_for("static", filename="docs/phase_1.4_CN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=5),
            },
            "1.5": {
                "type": "instructions",
                "english": url_for("static", filename="docs/phase_1.5_EN_instructions.pdf"),
                "mandarin": url_for("static", filename="docs/phase_1.5_CN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=6),
            },
            "1.6": {
                "type": "survey",
                "english_instructions": url_for("static", filename="docs/phase_1.6_EN_instructions.pdf"),
                "mandarin_instructions": url_for("static", filename="docs/phase_1.6_CN_instructions.pdf"),
                "english_survey": "https://umdsurvey.umd.edu/jfe/form/SV_26k2aVRuhtyVZsN", 
                "mandarin_survey": "https://umdsurvey.umd.edu/jfe/form/SV_baBQC9W2E36bSmh",
                "next": url_for("control", phase=2, subphase=0),
            },
            "2.0": {
                "type": "instructions",
                "english": url_for("static", filename="docs/phase_2.0_EN_instructions.pdf"),
                "mandarin": url_for("static", filename="docs/phase_2.0_CN_instructions.pdf"),
                "next": url_for("control", phase=2, subphase=1),
            },
            "2.1": {
                "type": "chat",
                "roomtype": "separate",
                "1cv1": url_for('static', filename='docs/user1_CV1.pdf'),
                "1cv2": url_for('static', filename='docs/user1_CV2.pdf'),
                "1cv3": url_for('static', filename='docs/user1_CV3.pdf'),
                "1cv4": url_for('static', filename='docs/user1_CV4.pdf'),
                "2cv1": url_for('static', filename='docs/user2_CV1.pdf'),
                "2cv2": url_for('static', filename='docs/user2_CV2.pdf'),
                "2cv3": url_for('static', filename='docs/user2_CV3.pdf'),
                "2cv4": url_for('static', filename='docs/user2_CV4.pdf'),
                "3cv1": url_for('static', filename='docs/user3_CV1.pdf'),
                "3cv2": url_for('static', filename='docs/user3_CV2.pdf'),
                "3cv3": url_for('static', filename='docs/user3_CV3.pdf'),
                "3cv4": url_for('static', filename='docs/user3_CV4.pdf'),
                "4cv1": url_for('static', filename='docs/user4_CV1.pdf'),
                "4cv2": url_for('static', filename='docs/user4_CV2.pdf'),
                "4cv3": url_for('static', filename='docs/user4_CV3.pdf'),
                "4cv4": url_for('static', filename='docs/user4_CV4.pdf'),
                "next": url_for("control", phase=3, subphase=3),
            },
            "3.0": {
                "type": "instructions",
                "english": url_for('static', filename='docs/phase_3.0_EN_instructions.pdf'),
                "mandarin": url_for("static", filename='docs/phase_3.0_CN_instructions.pdf'),
                "next": url_for("control", phase=3, subphase=1),
            },
            "3.1": {
                "type": "wait",
                "next": url_for("control", phase=3, subphase=2),
            },
            "3.2": {
                "type": "transcript",
                "next": url_for("control", phase=3, subphase=3),
            },
            "3.3": {
                "type": "survey",
                "english_instructions": url_for("static", filename="docs/phase_3.3_EN_instructions.pdf"),
                "mandarin_instructions": url_for("static", filename="docs/phase_3.3_CN_instructions.pdf"),
                "english_survey": "https://umdsurvey.umd.edu/jfe/form/SV_22Y0KXn6kgwZimN ",
                "mandarin_survey": "https://umdsurvey.umd.edu/jfe/form/SV_cAeRuGTx4FRLj1z",
                "next": url_for("control", phase=4, subphase=0),
            },
            "4.0": {
                "type": "instructions",
                "english": url_for('static', filename='docs/phase_4.0_EN_instructions.pdf'),
                "mandarin": url_for("static", filename="docs/phase_4.0_CN_instructions.pdf"),
                "next": url_for("control", phase=4, subphase=1),
            },
            "4.1": {
                "type": "chat",
                "roomtype": "not_separate",
                "1cv1": url_for('static', filename='docs/user1_CV1.pdf'),
                "1cv2": url_for('static', filename='docs/user1_CV2.pdf'),
                "1cv3": url_for('static', filename='docs/user1_CV3.pdf'),
                "1cv4": url_for('static', filename='docs/user1_CV4.pdf'),
                "2cv1": url_for('static', filename='docs/user2_CV1.pdf'),
                "2cv2": url_for('static', filename='docs/user2_CV2.pdf'),
                "2cv3": url_for('static', filename='docs/user2_CV3.pdf'),
                "2cv4": url_for('static', filename='docs/user2_CV4.pdf'),
                "3cv1": url_for('static', filename='docs/user3_CV1.pdf'),
                "3cv2": url_for('static', filename='docs/user3_CV2.pdf'),
                "3cv3": url_for('static', filename='docs/user3_CV3.pdf'),
                "3cv4": url_for('static', filename='docs/user3_CV4.pdf'),
                "4cv1": url_for('static', filename='docs/user4_CV1.pdf'),
                "4cv2": url_for('static', filename='docs/user4_CV2.pdf'),
                "4cv3": url_for('static', filename='docs/user4_CV3.pdf'),
                "4cv4": url_for('static', filename='docs/user4_CV4.pdf'),
                
                "next": url_for("control", phase=5, subphase=0),
            },
            "5.0": {
                "type": "survey",
                "english_instructions": url_for("static", filename="docs/phase_5.0_EN_instructions.pdf"),
                "mandarin_instructions": url_for("static", filename="docs/phase_5.0_CN_instructions.pdf"),
                "english_survey": "https://umdsurvey.umd.edu/jfe/form/SV_0xFKrg41yjC3H5r",
                "mandarin_survey": "https://umdsurvey.umd.edu/jfe/form/SV_3s0GDBme8QIVj4F",
                "next": None,
            },
        }
    
    return get_sitemap.sitemap

get_sitemap.sitemap = None


@app.route("/app/<phase>/<subphase>")
def control(phase, subphase):
    uid = session["uid"]
    username = users[uid - 1].username

    if uid == 1 or uid == 2:
        language = "mandarin"
    else:
        language = "english"

    site = get_sitemap()["{}.{}".format(phase, subphase)]

    if site["type"] == "user_specific_instructions":
        return render_template(
            "instructions.html", 
            uid=uid, 
            username=username, 
            file=site["user"+str(uid)], 
            next=site["next"]
        )
    elif site["type"] == "instructions":
        return render_template(
            "instructions.html", 
            uid=uid, 
            username=username, 
            file=site[language], 
            next=site["next"]
        )
    elif site["type"] == "survey":
        return render_template(
            "survey.html", 
            uid=uid, 
            username=username, 
            instructions=site[language+"_instructions"],
            survey=site[language+"_survey"], 
            next=site["next"]
        )
    elif site["type"] == "chat":
        if site["roomtype"] == "separate":
            room = "12" if uid == 1 or uid == 2 else "34"
        else:
            room = "1234"

        # Collect Posts
        posts = winter.models.Posts.query.filter(winter.models.Posts.room==room).order_by(asc(winter.models.Posts.timestamp)).all()

        # Collect Notes
        notes = notes = winter.models.Notes.query.filter(winter.models.Notes.uid == uid).first()
        notes = notes.notes if notes is not None else ""
        
        return render_template(
            "chat.html", 
            uid=uid, 
            username=username, 
            cv1=site[str(uid)+"cv1"], 
            cv2=site[str(uid)+"cv2"], 
            cv3=site[str(uid)+"cv3"], 
            cv4=site[str(uid)+"cv4"], 
            room=room,
            posts=posts,
            notes=notes,
            next=site["next"],
        )
    elif site["type"] == "wait": # TODO ****************************************
        return render_template(
            "phase_3.10_wait.html",
            uid=uid,
            username=username,
            next=site["next"],
        )
    elif site["type"] == "transcript": # TODO **********************************
        return render_template(
            "phase_3.1_transcript.html",
            uid=uid,
            username=username,
            next=site["next"],
        )


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
        
        post = winter.models.Posts(uid=data['uid'], username= data['username'], 
                                  body=data['msg'], time=data['time'], room=data['room'])
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
    emit('display', data, room=data['room'], include_self=False)


@app.route("/savenotes", methods=["PUT"])
def save_notes():
    uid = request.json["uid"]
    notes = request.json["notes"]

    new_notes = winter.models.Notes(uid=uid, notes=notes)
    
    db.session.merge(new_notes)
    db.session.commit()

    return '{"success": True}', 200, {"ContentType": "application/json"}