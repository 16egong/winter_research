// TODO Uncomment for deploy
document.addEventListener('DOMContentLoaded', () => {
    const pasteBox = document.getElementById("user-message");
    pasteBox.onpaste = e => {
        e.preventDefault();
        return false;
    };
})