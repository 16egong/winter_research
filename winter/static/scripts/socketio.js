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
            var style = ''
            if (data.uid == 1 || data.uid == 2) {
                style="background-image: url(https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fcdn-image.travelandleisure.com%2Fsites%2Fdefault%2Ffiles%2Fstyles%2F1600x1000%2Fpublic%2Fblue0517.jpg%3Fitok%3DV3825voJ&w=400&c=sc&poi=face&q=85)"
            } else {
                style="background-image: url(https://www.macmillandictionary.com/external/slideshow/full/Lime%20Green_full.png)"
            }
            const msgHTML = `
                <div class="msg ${side}-msg">
                    <div class="msg-img" style="${style}">
                    </div>
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