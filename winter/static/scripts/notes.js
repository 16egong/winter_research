var timer;

document.addEventListener("DOMContentLoaded", () => {
    $("#note-textbox").on("input", notesChanged);
    // TODO: Uncomment below for deploy
    // setInterval(function(){ saveRecord(uid, $("#note-textbox").val()); }, 15000);
      

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

function saveRecord(uid, record) {
    data = {
        uid: uid,
        record: record,
    }

    $.ajax({
        type: "PUT",
        url: recordurl,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: recordUpdateSuccess,
        error: recordUpdateFailure,
    })
}

function notesUpdateSuccess(data) {
    console.log("successfully updated notes")
}

function notesUpdateFailure(data) {
    console.log("failed to update notes")
}

function recordUpdateSuccess(data) {
    console.log("successfully updated record")
}

function recordUpdateFailure(data) {
    console.log("failed to update record")
}