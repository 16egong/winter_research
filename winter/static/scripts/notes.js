var timer;

document.addEventListener("DOMContentLoaded", () => {
    $("#note-textbox").on("input", notesChanged);
})

function notesChanged() {
    clearTimeout(timer);

    timer = setTimeout(() => {
        updateNotes(uid, $("#note-textbox").val());
    }, 500)
}

function updateNotes(uid, notes) {
    data = {
        uid: uid,
        notes: notes,
    }

    $.ajax({
        type: "PUT",
        url: notesurl,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: notesUpdateSuccess,
        error: notesUpdateFailure,
    })
}

function notesUpdateSuccess(data) {
    console.log("successfully updated notes")
}

function notesUpdateFailure(data) {
    console.log("failed to update notes")
}