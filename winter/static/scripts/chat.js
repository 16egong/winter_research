const pasteBox = document.getElementById("user-message");
  pasteBox.onpaste = e => {
    e.preventDefault();
    return false;
  };