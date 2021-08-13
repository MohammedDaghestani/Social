$('.submenu').click(function(){
    let index = $(this).index();
    // let submenu = $('.submenu').eq(index)
    let body = $(this).find('.submenu-body');
    let title = $(this).find('.submenu-title');
    let chevron = $(title).find('.fa-chevron-right')

    if(body.css('display') == 'block'){
        body.slideUp(200);
        chevron.removeClass("down");
    } else {
        $('.submenu-body').slideUp(200);
        $('.rotate').removeClass('down');
        chevron.addClass("down");
        body.slideDown(200);
    }
});