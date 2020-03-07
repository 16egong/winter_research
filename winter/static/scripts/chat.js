document.addEventListener('DOMContentLoaded', () => {
    const pasteBox = document.getElementById("user-message");
    pasteBox.onpaste = e => {
        e.preventDefault();
        return false;
    };
})

function showPage(page_num) {
    $('.cv').removeClass('active');
    $('.page').removeClass('active');
    var $cv = $('#'+page_num + '.cv');
    var $page = $('#'+page_num + '.page');
    $cv.addClass('active');
    $page.addClass('active');
}

function nextPage() {
    var $cur_cv = $('.cv.active');
    var $cur_num = $('.page.active');
    if($cur_cv.next().is('iframe')) {
        $('.cv').removeClass('active');
        $cur_cv.next().addClass('active');
        $('.page').removeClass('active');
        $cur_num.next().addClass('active');
    }
}

function prevPage() {
    var $cur_cv = $('.cv.active');
    var $cur_num = $('.page.active');
    if($cur_cv.prev().is('iframe')) {
        $('.cv').removeClass('active');
        $cur_cv.prev().addClass('active');
        $('.page').removeClass('active');
        $cur_num.prev().addClass('active');
    }
    
}