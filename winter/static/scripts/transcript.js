document.addEventListener("DOMContentLoaded", () => {
    set_timer(10)
})

function set_timer(time_in_min) {
    var clock = document.getElementById('counter');
    var current_time = Date.parse(new Date());
    var endtime = new Date(current_time + time_in_min*60*1000);
    run_clock(clock, endtime);
}

function time_remaining(endtime){
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor( (t/1000) % 60 );
    var minutes = Math.floor( (t/1000/60) % 60 );
    var hours = Math.floor( (t/(1000*60*60)) % 24 );
    var days = Math.floor( t/(1000*60*60*24) );
    return {'total':t, 'days':days, 'hours':hours, 'minutes':minutes, 'seconds':seconds};
}

function run_clock(clock, endtime){
    function update_clock(){
        var t = time_remaining(endtime);
        clock.innerHTML = 'Time Left: '+t.minutes+': '+t.seconds;
        if(t.total<=0){
            clearInterval(timeinterval);
            clock.innerHTML = 'Times Up!';
            const msg = document.getElementById("user-message");
            msg.onkeypress = e => {
                e.preventDefault();
            };
         }
    }
    update_clock();
    var timeinterval = setInterval(update_clock,1000);
}

function showPage(page_num) {
    $('.block').removeClass('active');
    $('.page').removeClass('active');
    var $msg = $('.'+page_num + '.block');
    var $page = $('.'+page_num + '.page');
    $msg.addClass('active');
    $page.addClass('active');
}

function nextPage() {
    var $cur_msg = $('.block.active');
    var $cur_num = $('.page.active');
    if($cur_msg.next().is('section')) {
        $('.block').removeClass('active');
        $cur_msg.next().addClass('active');
        $('.page').removeClass('active');
        $cur_num.next().addClass('active');
    }
}

function prevPage() {
    var $cur_msg = $('.block.active');
    var $cur_num = $('.page.active');
    if($cur_msg.prev().is('section')) {
        $('.block').removeClass('active');
        $cur_msg.prev().addClass('active');
        $('.page').removeClass('active');
        $cur_num.prev().addClass('active');
    }
    
}