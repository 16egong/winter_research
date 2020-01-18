from flask import session, render_template
from flask_socketio import emit, send
from winter import app
from winter import socketio
from winter import db
import winter.models
import winter.users
from sqlalchemy import asc
import pandas as pd
import config

# db = SQLAlchemy(app)

# from app import routes, models

@app.route('/1',methods = ['POST', 'GET'])
def chat1():
    user = winter.users.User(uid=1, username='Tyler', real_name='Pablo E.')
    posts =  winter.models.Post.query.order_by(asc(winter.models.Post.timestamp)).all()
    usernames = []
    for p in posts:
        if p.username not in usernames:
            usernames.append(p.username)
            
    print('Usernames: ', usernames)
    return render_template("chat.html", uid=user.uid, username=user.username, real_name=user.real_name, posts=posts, usernames=usernames)


@app.route('/2',methods = ['POST', 'GET'])
def chat2():
    user = winter.users.User(uid=2, username='Charlie', real_name='Tyrone S.')
    posts =  winter.models.Post.query.order_by(asc(winter.models.Post.timestamp)).all()
    usernames = []
    
    for p in posts:
        if p.username not in usernames:
            usernames.append(p.username)
            
    print('Usernames: ', usernames)
    return render_template("chat.html", uid=user.uid, username=user.username, real_name=user.real_name, posts=posts, usernames=usernames)

@app.route('/3',methods = ['POST', 'GET'])
def chat3():
    user = winter.users.User(uid=3, username='Sam', real_name='Elion R.')
    posts =  winter.models.Post.query.order_by(asc(winter.models.Post.timestamp)).all()
    usernames = []
    for p in posts:
        if p.username not in usernames:
            usernames.append(p.username)
            
    return render_template("chat.html", uid=user.uid, username=user.username, real_name=user.real_name, posts=posts)

@app.route('/4',methods = ['POST', 'GET'])
def chat4():
    user = winter.users.User(uid=4, username='Jamie', real_name='Cindy L.')
    posts =  winter.models.Post.query.order_by(asc(winter.models.Post.timestamp)).all()
    usernames = []
    for p in posts:
        if p.username not in usernames:
            usernames.append(p.username)
            
    return render_template("chat.html", uid=user.uid, username=user.username, real_name=user.real_name, posts=posts)

@app.route('/transcript')
def transcript():
    posts =  winter.models.Post.query.order_by(asc(winter.models.Post.timestamp)).all()
    return render_template("transcript.html", posts=posts)
    
    
@socketio.on('message')
def message(data):
    try:
        print('MESSAGE')
        print(f'\n\n{data}\n\n')
        post = winter.models.Post(uid=data['uid'], username= data['username'], 
                                  real_name=data['real_name'], body=data['msg'])
        db.session.add(post)
        db.session.commit()

#         posts = winter.models.Post.query.all()
#         for p in posts:
#             print('POST')
#             print(p.id, p.username, p.body, p.timestamp)
        # add timestamp
        # gets sent to the message bucket on client side
        send(data, broadcast=True)
    except Exception as e:
        print('ELSE: ', e )
        print(f'\n\n{data}\n\n')
        send(data, broadcast=True)
    
    
# if __name__ == '__main__':
#     socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')
    # socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')