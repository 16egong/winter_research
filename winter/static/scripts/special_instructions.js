// TODO Uncomment for deploy
function showPage(page_num) {
    $('.instr').removeClass('active');
    $('.page').removeClass('active');
    var $instr = $('.'+page_num + '.instr');
    var $page = $('.'+page_num + '.page');
    $instr.addClass('active');
    $page.addClass('active');
    $page.addClass('check');

    if ($('.page.0').hasClass('check') && $('.page.1').hasClass('check') 
    && $('.page.2').hasClass('check'))
    {
        
        $('#next').prop('disabled', false);
        $('#next').css('background-color', '#4CAF50');
    } 
}

function nextPage() {
    var $cur_instr = $('.instr.active');
    var $cur_num = $('.page.active');
    if($cur_instr.next().is('iframe')) {
        $('.instr').removeClass('active');
        $cur_instr.next().addClass('active');
        $('.page').removeClass('active');
        $cur_num.next().addClass('active');
        $cur_num.next().addClass('check');
    }

    if ($('.page.1').hasClass('check') && $('.page.1').hasClass('check') 
    && $('.page.2').hasClass('check'))
    {
        $('#next').prop('disabled', false);
        $('#next').css('background-color', '#4CAF50');
    } 
}

function prevPage() {
    var $cur_instr = $('.instr.active');
    var $cur_num = $('.page.active');
    if($cur_instr.prev().is('iframe')) {
        $('.instr').removeClass('active');
        $cur_instr.prev().addClass('active');
        $('.page').removeClass('active');
        $cur_num.prev().addClass('active');
        $cur_num.prev().addClass('check');
    }

    if ($('.page.1').hasClass('check') && $('.page.1').hasClass('check') 
    && $('.page.2').hasClass('check'))
    {
        $('#next').prop('disabled', false);
        $('#next').css('background-color', '#4CAF50');
    } 
}

function clickNext() { 
    if (!$('#next').is(':disabled')) {
        window.open(next, "_self"); 
    } else{
        console.log("Please click the survey first");
    }
};