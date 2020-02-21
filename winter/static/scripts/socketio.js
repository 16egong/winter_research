document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    let msg = document.getElementById("user-message");
    var typing = false;
    var timeout = undefined;
    // Autofocus on textbox
    document.querySelector("#user-message").focus();
    
    
    // Client Connects
    socket.on('connect', () => {
        socket.emit('join', {'username': username, 'room': room}); 
        console.log(`Message recieved: User Connected`);
    });
    
    // Message handler for the 'join_room' channel
    socket.on('join_room', function(msg) {
        console.log(`Join room: ${msg}`);
    });
    
    socket.on('display', data =>{
        const typing_id = `typing_on${data.uid}`
        const typing_on = document.getElementById(typing_id);
        
        if(data.typing==true){
            typing_on.innerHTML = '<p><em>' + data.username + ' is typing a message...</em></p>';
        } else {
            typing_on.innerHTML = ""
        }
    });
    
    // End typing status
    function typingTimeout(){
        typing=false
        socket.emit('typing', {'username':username, 'uid': uid, 'typing':false, 'room':room})
    }
    // Checking copy paste
//     function checkPaste(key) {
//         var ctrlDown = false,
//         ctrlKey = 17,
//         cmdKey = 91,
//         vKey = 86,
//         cKey = 67;
        
//         if ((key == ctrlKey || key == cmdKey)) {
//             ctrlDown = true;
//         }
//         if (key == ctrlKey || key == cmdKey) {
//             ctrlDown = false;
//         }
        
//     });
        
    
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
    
    // Event listener
    msg.addEventListener('keypress', function(e){
        checkTypingStatus(e.keyCode)
    })
})