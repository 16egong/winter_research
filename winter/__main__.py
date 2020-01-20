import os

if __name__ == "__main__":
    from winter import db, app, socketio
    import winter.models
    import winter.users
    
    if os.environ.get('PORT') is not None:
        socketio.run(app, debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        socketio.run(app, debug=True, host='0.0.0.0') 

