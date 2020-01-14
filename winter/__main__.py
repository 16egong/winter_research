if __name__ == "__main__":
    from winter import db, app, socketio
    import winter.models
    import winter.users
    
    
#     p2 = winter.users.User(uid=2, username='Charlie', real_name='Tyrone S.')
#     p1 = winter.models.User(id=1, username='Sam', real_name='Pablo E.')
#     p2 = winter.models.User(id=2, username='Charlie', real_name='Tyrone S.')

#     db.session.merge(p1)
#     db.session.merge(p2)
#     db.session.commit()
    
#     print('Before SocketIO Run')
    
#     socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0')
#     app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0')