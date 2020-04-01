function showPage(page_num) {
    var $curr_msg = $('.block.active');
    var $page_num = $('.page.active');
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
    if($cur_msg.next().is('div')) {
        $('.block').removeClass('active');
        $cur_msg.next().addClass('active');
        $('.page').removeClass('active');
        $cur_num.next().addClass('active');
    }
}

function prevPage() {
    var $cur_msg = $('.block.active');
    var $cur_num = $('.page.active');
    if($cur_msg.prev().is('div')) {
        $('.block').removeClass('active');
        $cur_msg.prev().addClass('active');
        $('.page').removeClass('active');
        $cur_num.prev().addClass('active');
    }
    
}