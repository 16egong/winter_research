document.addEventListener('DOMContentLoaded', () => {
    // Make 'enter' key submit message
    let msg = document.getElementById("user-message");
    msg.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("send-message").click();
        }
    });
    //Make @ butt create a dropdown
});