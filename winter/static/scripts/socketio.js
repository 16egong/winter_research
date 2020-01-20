// Will later update to jquery
document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    
    // Autofocus on textbox
    document.querySelector("#user-message").focus();
    
//     client connects and sends message to server message bucket
    socket.on('connect', () => {
        socket.emit('join', {'username': username, 'room': room}); 
//         socket.send(data={'msg': username + ' has joined the chat'}, room=room);
        console.log(`Message recieved: User Connected`);
    });
    
    // message handler for the 'join_room' channel
    socket.on('join_room', function(msg) {
        console.log(msg);
    });
    
    socket.on('message', data => {
//         var obj = JSON.parse(data)
        if (data.username) {
            const p = document.createElement('p');
            const msgerChat = document.querySelector(".msger-chat")
            var side = ''
            if (data.username == username) {
                side = 'right'
            } else {
                side = 'left'
            }
            const msgHTML = `
                <div class="msg ${side}-msg">
                  <div class="msg-bubble">
                    <div class="msg-info">
                      <div class="msg-info-name">${data.username}</div>
                      <div class="msg-info-time">${data.time}</div>
                    </div>
                    <div class="msg-text">${data.msg}</div>
                  </div>
                </div>
              `;
            msgerChat.insertAdjacentHTML("beforeend", msgHTML);
            msgerChat.scrollTop += 500;
            
//             p.classList.add("message");
//             const br = document.createElement('br');
//             p.innerHTML = data.username + ": " + data.msg;
//     //         p.innerHTML = data;
//             document.querySelector('#messages').append(p)
        } else {
            const p = document.createElement('p');
            p.innerHTML = data.msg;
            p.classList.add("message");
            document.querySelector('#messages').append(p)
        }
        console.log(`Message recieved: ${data}`);
    })
    
    // Send Message
    document.querySelector('#send-message').onclick = () => {
        console.log(`To be sent to server: ${ document.querySelector('#user-message').value}`)
        socket.send({'uid': uid, 'username': username, 'msg': document.querySelector('#user-message').value, 'room': room}); 
        // Clear Input
        document.querySelector('#user-message').value = ''
    }
})