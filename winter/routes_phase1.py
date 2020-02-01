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

# db = SQLAlchemy(app)

# from app import routes, models
@app.route('/1')
def inst1():
    user = config.USER1
    url = url_for('chat1')
    return render_template("instructions.html", uid=user.uid, url=url)


@app.route('/2')
def inst2():
    user = config.USER2
    url = url_for('chat2')
    return render_template("instructions.html", uid=user.uid, url=url)


@app.route('/3')
def inst3():
    user = config.USER3
    url = url_for('chat3')
    return render_template("instructions.html", uid=user.uid, url=url)


@app.route('/4')
def inst4():
    user = config.USER4
    url = url_for('chat4')
    return render_template("instructions.html", uid=user.uid, url=url)
    
    
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


@app.route('/transcript_12')
def transcript_12():
    posts =  winter.models.Post.query.filter(or_(winter.models.Post.uid == 1, winter.models.Post.uid == 2)).order_by(asc(winter.models.Post.timestamp)).all()
    return render_template("transcript.html", posts=posts)


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
    emit('join_room' {'msg': username + ' has entered the room.'}, room=room)
    
    
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
    print('\ntyping!!! ', data)
    emit('typing', data['username'], room=data['room'], include_self=True)
    
# if __name__ == '__main__':
#     socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')
    # socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')