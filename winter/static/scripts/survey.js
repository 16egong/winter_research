function clickSurvey() {
//     window.location.href = survey;
    console.log(`Survey: ${survey}`);
    window.open(survey, '_blank');
    $('#survey').prop('disabled', true);
    $('#survey').css('background-color', '#dfdfdf');
    $('#next').prop('disabled', false);
    $('#next').css('background-color', '#4CAF50');
    
    
};

function clickNext() { 
    if ($('#survey').is(':disabled')) {
        window.open(next, "_self"); 
    } else{
        console.log("Please click the survey first");
    }
    
};
