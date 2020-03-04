function clickSurvey() {
//     window.location.href = survey;
    console.log(`Survey: ${survey}`)
    window.open(survey, '_blank');
    $('#survey').prop('disabled', true);
    $('#survey').css('background-color', '#dfdfdf');
    $('#next').prop('disabled', false);
    $('#next').css('background-color', '#4CAF50');
    
    
};
function clickNext() {
    window.open(next, "_self");
};



// function clickButton(page_num) {
//     var $curr_msg = $('.block.active');
//     var $page_num = $('.page.active');
//     $('.block').removeClass('active');
//     $('.page').removeClass('active');
//     var $msg = $('#'+page_num + '.block');
//     var $page = $('#'+page_num + '.page');
//     $msg.addClass('active');
//     $page.addClass('active');
// }

// $("#survey").click(function (event) {
//     if ($(this).hasClass("disabled")) {
//         event.preventDefault();
//     }
//     $(this).addClass("disabled");
//     document.getElementById("next").disabled = false;
// });