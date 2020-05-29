from flask import request, session, render_template, redirect, url_for
from flask_socketio import emit, send, join_room, leave_room
from winter import app
from winter import socketio
from winter import db
import winter.models
from sqlalchemy import asc, or_
import config
import time
from datetime import datetime
import pytz
import requests
import logging
import threading


logger = logging.getLogger()
    
@app.route('/<int:uid>')
def base(uid):
    session["uid"] = uid

    return redirect(url_for("control", phase=0, subphase=0))

users = [config.USER1, config.USER2, config.USER3, config.USER4, config.USER12, config.USER34]

def get_sitemap():
    """ A bit of a hack to get this dictionary to be properly populated """
    if get_sitemap.sitemap is None:
        get_sitemap.sitemap = {
            "0.0": {
                "type": "wait",
                "english": url_for("static", filename="docs/phase_0.0_EN_wait.pdf"),
                "mandarin": url_for("static", filename="docs/phase_0.0_CN_wait.pdf"),
                "next": url_for("control", phase=1, subphase=0),
            },
            "1.0": {
                "type": "user_specific_instructions",
                "user1": url_for("static", filename="docs/phase_1.0_user_1_CN_instructions.pdf"),
                "user2": url_for("static", filename="docs/phase_1.0_user_2_CN_instructions.pdf"),
                "user3": url_for("static", filename="docs/phase_1.0_user_3_EN_instructions.pdf"),
                "user4": url_for("static", filename="docs/phase_1.0_user_4_EN_instructions.pdf"),
                "user12": url_for("static", filename="docs/phase_1.0_user_1_CN_instructions.pdf"),
                "user34": url_for("static", filename="docs/phase_1.0_user_3_EN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=1),
            },
            "1.1": {
                "type": "instructions",
                "english": url_for("static", filename="docs/phase_1.1_EN_instructions.pdf"),
                "mandarin": url_for("static", filename="docs/phase_1.1_CN_instructions.pdf"),
                "next": url_for("control", phase=1, subphase=2),
            },
            "1.2": {
                "type": "special_instructions",
                "user1": url_for("static", filename="docs/phase_1.2_user_1_CN_instructions.pdf"),
                "user2": url_for("static", filename="docs/phase_1.2_user_2_CN_instructions.pdf"),
                "user3": url_for("static", filename="docs/phase_1.2_user_3_EN_instructions.pdf"),
                "user4": url_for("static", filename="docs/phase_1.2_user_4_EN_instructions.pdf"),
                "user12": url_for("static", filename="docs/phase_1.2_user_1_CN_instructions.pdf"),
                "user34": url_for("static", filename="docs/phase_1.2_user_3_EN_instructions.pdf"),
                "english_1": url_for("static", filename="docs/phase_1.3_EN_instructions.pdf"),
                "mandarin_1": url_for("static", filename="docs/phase_1.3_CN_instructions.pdf"),
                "english_2": url_for("static", filename="docs/phase_1.4_EN_instructions.pdf"),
                "mandarin_2": url_for("static", filename="docs/phase_1.4_CN_instructions.pdf"),

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
                "12cv1": url_for('static', filename='docs/user1_CV1.pdf'),
                "12cv2": url_for('static', filename='docs/user1_CV2.pdf'),
                "12cv3": url_for('static', filename='docs/user1_CV3.pdf'),
                "12cv4": url_for('static', filename='docs/user1_CV4.pdf'),
                "34cv1": url_for('static', filename='docs/user3_CV1.pdf'),
                "34cv2": url_for('static', filename='docs/user3_CV2.pdf'),
                "34cv3": url_for('static', filename='docs/user3_CV3.pdf'),
                "34cv4": url_for('static', filename='docs/user3_CV4.pdf'),
                "chat": False,
                "next": url_for("control", phase=2, subphase=2),
            },
            "2.2": {
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
                "12cv1": url_for('static', filename='docs/user1_CV1.pdf'),
                "12cv2": url_for('static', filename='docs/user1_CV2.pdf'),
                "12cv3": url_for('static', filename='docs/user1_CV3.pdf'),
                "12cv4": url_for('static', filename='docs/user1_CV4.pdf'),
                "34cv1": url_for('static', filename='docs/user3_CV1.pdf'),
                "34cv2": url_for('static', filename='docs/user3_CV2.pdf'),
                "34cv3": url_for('static', filename='docs/user3_CV3.pdf'),
                "34cv4": url_for('static', filename='docs/user3_CV4.pdf'),
                "chat": True,
                "next": url_for("control", phase=3, subphase=0),
            },
            "3.0": {
                "type": "instructions",
                "english": url_for('static', filename='docs/phase_3.0_EN_instructions.pdf'),
                "mandarin": url_for("static", filename='docs/phase_3.0_CN_instructions.pdf'),
                "next": url_for("control", phase=3, subphase=1),
            },
            "3.1": {
                "type": "wait",
                "english": url_for("static", filename="docs/phase_0.0_EN_wait.pdf"),
                "mandarin": url_for("static", filename="docs/phase_0.0_CN_wait.pdf"),
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
                "12cv1": url_for('static', filename='docs/user1_CV1.pdf'),
                "12cv2": url_for('static', filename='docs/user1_CV2.pdf'),
                "12cv3": url_for('static', filename='docs/user1_CV3.pdf'),
                "12cv4": url_for('static', filename='docs/user1_CV4.pdf'),
                "34cv1": url_for('static', filename='docs/user3_CV1.pdf'),
                "34cv2": url_for('static', filename='docs/user3_CV2.pdf'),
                "34cv3": url_for('static', filename='docs/user3_CV3.pdf'),
                "34cv4": url_for('static', filename='docs/user3_CV4.pdf'),
                "chat": True,
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

    if uid == 12:
        username = users[4].username
    elif uid == 34:
        username=users[5].username
    else:
        username=users[uid - 1].username

    if uid == 1 or uid == 2 or uid == 12:
        language="mandarin"
    else:
        language="english"

    site = get_sitemap()["{}.{}".format(phase, subphase)]

    
    if site["type"] == "instructions":
        return render_template(
            "instructions.html", 
            uid=uid, 
            username=username, 
            file=site[language],
            next=site["next"]
        )
    elif site["type"] == "user_specific_instructions":
        return render_template(
            "instructions.html", 
            uid=uid, 
            username=username, 
            file=site["user"+str(uid)], 
            next=site["next"]
        )
    elif site["type"] == "special_instructions":
        return render_template(
            "special_instructions.html",
            uid=uid,
            username=username,
            inst1_2=site["user"+str(uid)],
            inst1_3=site[language+"_1"],
            inst1_4=site[language+"_2"],
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
            room = "12" if uid == 1 or uid == 2 or uid == 12 else "34"
            session["room"] = room 
        else:
            room="1234"
            session["room"] = room

        # Collect Posts
        posts = winter.models.Posts.query.filter(winter.models.Posts.room==room).order_by(asc(winter.models.Posts.timestamp)).all()

        # Collect Notes
        notes = notes = winter.models.Notes.query.filter(winter.models.Notes.uid == uid).first()
        notes = notes.notes if notes is not None else ""
        
        return render_template(
            "chat.html", 
            uid=uid, 
            username=username, 
            chat=site["chat"],
            cv1=site[str(uid)+"cv1"], 
            cv2=site[str(uid)+"cv2"], 
            cv3=site[str(uid)+"cv3"], 
            cv4=site[str(uid)+"cv4"], 
            room=room,
            posts=posts,
            notes=notes,
            next=site["next"]
        )
    elif site["type"] == "wait": 
        return render_template(
            "wait.html",
            uid=uid,
            username=username,
            file=site[language], 
            next=site["next"]
        )
    elif site["type"] == "transcript":

        room = "12" if uid == 3 or uid == 4 or uid == 34 else "34"

        # Collect Posts
        posts = winter.models.Posts.query.filter(winter.models.Posts.room==room).order_by(asc(winter.models.Posts.timestamp)).all()
        
        # Collect Notes
        notes = notes = winter.models.Notes.query.filter(winter.models.Notes.uid == uid).first()
        notes = notes.notes if notes is not None else ""

        return render_template(
            "transcript.html",
            uid=uid,
            username=username,
            room=room,
            posts=posts,
            notes=notes,
            next=site["next"]
        )


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    if username != 'Yongle 12' and username != 'Yongle 34':
        if username not in config.ROOMS[room]:
            config.ROOMS[room].append(username)
        logger.critical('ROOMS AFTER %s', config.ROOMS)
        if room == "1234":
            if len(config.ROOMS[room]) == 4:
                logger.critical('START TIMER 4')
                emit('start_timer', {'time': 15, 'users': config.ROOMS[room]}, room=room)
        else:
            if len(config.ROOMS[room]) == 2:
                logger.critical('START TIMER 2')
                emit('start_timer', {'time': 15, 'users': config.ROOMS[room]}, room=room)

    emit('join_room', {'user': username + ' has entered the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    config.ROOMS[room].remove(username)
    logger.critical('ROOMS AFTER LEAVE %s', config.ROOMS)
    emit('leave_room', {'user': username + ' has left the room.'}, room=room)


@socketio.on('message')
def message(data):
    try:
        logger.critical('SERVER SIDE MESSAGE')
        tz = pytz.timezone('US/Eastern')
        data['time'] = str(datetime.now(tz).strftime('%I:%M %p'))

        post = winter.models.Posts(uid=data['uid'], username= data['username'], 
                                  body=data['msg'], time=data['time'], room=data['room'])
        
        db.session.add(post)
        db.session.commit()

        # gets sent to the message bucket on client side
        room = data['room']
        send(data, room=room)
        logger.critical('\n\n %s \n\n', data)
    except Exception as e:
        logger.critical('ELSE: %s', e )
        logger.critical('\n\n %s \n\n', data)
        send(data, room=room)

# Present typing message
@socketio.on('typing')
def typing(data):
    emit('display', data, room=data['room'], include_self=False)

# Save notes
@app.route("/savenotes", methods=["PUT"])
def save_notes():
    uid = request.json["uid"]
    notes = request.json["notes"]

    new_notes = winter.models.Notes(uid=uid, notes=notes)
    
    db.session.merge(new_notes)
    db.session.commit()

    return '{"success": True}', 200, {"ContentType": "application/json"}

# Save notes in intervals
@app.route("/saverecord", methods=["PUT"])
def save_record():
    uid = request.json["uid"]
    record = request.json["record"]

    current_record = winter.models.Record(uid=uid, record=record)
    
    db.session.add(current_record)
    db.session.commit()

    return '{"success": True}', 200, {"ContentType": "application/json"}
