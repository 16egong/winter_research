document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port );
    let msg = document.getElementById("user-message");
    var typing = false;
    var timeout = undefined;

    // Autofocus on textbox
    document.querySelector("#user-message").focus();
    
    // Client Connects
    socket.on('connect', () => {
        socket.emit('join', {'username': username, 'room': room}); 
        console.log(`User Connecting`);
        socket.on('disconnect', function () {
            socket.emit('leave', {'username': username, 'room': room});
            console.log(`User Disconnected: ${username}`);
          });
    });

    // Message handler for the 'join_room' channel
    socket.on('join_room', data => {
        console.log(`Join room: ${data.user}`);
    });

    // Message handler for the 'leave_room' channel
    socket.on('leave_room', data => {
        console.log(`Left room: ${data.user}`);
    });

    // Start timer
    socket.on('start_timer', data => {
        console.log(`DEBUG: users in room ${data.users}`);
        console.log(`DEBUG: start timer ${data.time}`);
        set_timer(data.time)
    });

    function set_timer(time_in_min) {
        var clock = document.getElementById('counter');
        var current_time = Date.parse(new Date());
        var endtime = new Date(current_time + time_in_min*60*1000);
        run_clock(clock, endtime);
    }

    function time_remaining(endtime){
        var t = Date.parse(endtime) - Date.parse(new Date());
        var seconds = Math.floor( (t/1000) % 60 );
        var minutes = Math.floor( (t/1000/60) % 60 );
        var hours = Math.floor( (t/(1000*60*60)) % 24 );
        var days = Math.floor( t/(1000*60*60*24) );
        return {'total':t, 'days':days, 'hours':hours, 'minutes':minutes, 'seconds':seconds};
    }
    
    function run_clock(clock, endtime){
        function update_clock(){
            var t = time_remaining(endtime);
            clock.innerHTML = 'Time Left: '+t.minutes+': '+t.seconds;
            if(t.total<=0){
                clearInterval(timeinterval);
                clock.innerHTML = 'Times Up!';
                const msg = document.getElementById("user-message");
                msg.onkeypress = e => {
                    e.preventDefault();
                };
             }
        }
        update_clock();
        var timeinterval = setInterval(update_clock,1000);
    }
    
    // Displaying typing status
    socket.on('display', data =>{
        const typing_id = `typing_on${data.uid}`
        const typing_on = document.getElementById(typing_id);
        
        if(data.typing==true){
            typing_on.innerHTML = '<p><em>' + data.username + ' is typing a message...</em></p>';
            typing_on.className = 'shown'
        } else {
            typing_on.innerHTML = ""
            typing_on.className = 'hidden'
        }
    });
    
    // End typing status
    function typingTimeout(){
        typing=false
        socket.emit('typing', {'username':username, 'uid': uid, 'typing':false, 'room':room})
    }
        
    
    // Check typing status
    function checkTypingStatus(key) {
        var enterKey = 13;

        if(key !== enterKey){
            typing=true
            socket.emit('typing', {'username': username, 'uid': uid, 'typing': true, 'room': room});
            clearTimeout(timeout)
            timeout=setTimeout(typingTimeout, 1500)
        } else {
            clearTimeout(timeout)
            typingTimeout()
            document.getElementById("send-message").click();
        }
    }
    
    // Message handler
    socket.on('message', data => {
        console.log(`CLIENT SIDE Message recieved: ${data}`);
        try {
            if (data.username) {
                const msgerChat = document.getElementById("messages")
                var side = ''
                if (data.username == username) {
                    side = 'sender'
                } else {
                    side = 'receiver'
                } 
                var style = ''
                if (data.uid == 1 || data.uid == 2) {
                    style="background-image: url(https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fcdn-image.travelandleisure.com%2Fsites%2Fdefault%2Ffiles%2Fstyles%2F1600x1000%2Fpublic%2Fblue0517.jpg%3Fitok%3DV3825voJ&w=400&c=sc&poi=face&q=85)"
                } else {
                    style="background-image: url(https://www.macmillandictionary.com/external/slideshow/full/Lime%20Green_full.png)"
                }
                const msgHTML = `
                    <div class="message ${side}">
                        <div class="message-image" style="${style}">
                        </div>
                        <div class="message-bubble">
                            <div class="message-info">
                                <div class="message-info-name">${data.username}</div>
                                <div class="message-info-time">${data.time}</div>
                            </div>
                        <div class="message-text">${data.msg}</div>
                    </div>
                    </div>
                `;
                msgerChat.insertAdjacentHTML("beforeend", msgHTML);
                msgerChat.scrollTop += 500;
                
            } else {
                console.log('DOES THIS EVER HAPPEN IN SOCKETIO JS? USER NO USER ID')
                const p = document.createElement('p');
                p.innerHTML = data.msg;
                p.classList.add("message");
                document.querySelector('#messages').append(p)
            }
            console.log(`MESSAGE RECIEVED AND COMPLETE: ${data}`);
        } catch(err) {
            console.log(`ERROR OF SOME SORT: ${err.messageta}`);
        }

        
    })
    
    // Send Message
    document.querySelector('#send-message').onclick = () => {
        console.log('SEND MESSAGE: CLIENT SIDE \n')
        console.log(`To be sent to server: ${ document.querySelector('#user-message').value}`)
        socket.send({'uid': uid, 'username': username, 'msg': document.querySelector('#user-message').value, 'room': room}); 
        
        // Clear Input
        document.querySelector('#user-message').value = ''
    }
    
    // Event listener
    msg.addEventListener('keypress', function(e){
        checkTypingStatus(e.keyCode)
    })
})