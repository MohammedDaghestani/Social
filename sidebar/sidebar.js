// $(document).ready(function(){
    // if($(window).width() <= '750'){
    //     $('#toggler').removeClass('maximize');
    //     $('#toggler').removeClass('activeToggle');
    //     $(".sidebar").removeClass('expended');
    //     $(".sidebar").removeClass('shadow-lg');
    //     $('body').addClass('full');
    // }
// });

$('.sidebar-section-item-title').click(function(){
    // let index = $(this).index();
    // let submenu = $('.submenu').eq(index)
    let parent = $(this).parent();
    let body = $(parent).find('.sidebar-section-item-body');
    let title = $(this)
    let chevron = $(title).find('.fa-chevron-right')

    if(body.css('display') == 'block'){
        body.slideUp(200);
        chevron.removeClass("down");
    } else {
        $('.sidebar-section-item-body').slideUp(200);
        $('.rotate').removeClass('down');
        chevron.addClass("down");
        body.slideDown(200);
    }
});
// function sidebarToggle(){
//     $('#toggler').toggleClass('activeToggle');
//     // $(".sidebar").toggleClass('expended');
//     $(".sidebar").toggleClass('shadow-lg');
//     // $('#toggler').toggleClass('expended');
//     // $('body').toggleClass('full');
// }
$('#toggler').click(function(){
    if($(window).width() > '750'){
        sidebarToggleMaxWidth();
    } else{
        sidebarToggleMinWidth();
    }

})
// $( window ).resize(function() {
//     if($( window ).width() <= '750'){
//         // $('#toggler').removeClass('maximize');
//         // $('#toggler').removeClass('activeToggle');
//         // $(".sidebar").removeClass('expended');
//         // $(".sidebar").removeClass('shadow-lg');
//         // $('body').addClass('full');
//     } else {
//         $('#toggler').addClass('maximize');
//     }
// });

// function sidebar(){
//     // alert($('.sidebar').css('left'))
//     if($('.sidebar').css('left') == '0px'){
//         $('.sidebar').css('left', '-15rem');
//         $('.sidebar').css('display', 'none');
//         // $('body').css('margin-left', '0')
//     } else {
//         $('.sidebar').css('display', 'block');
//         $('.sidebar').css('left', '0');
//         // $('body').css('margin-left', '15rem')
//     }
// }
function sidebarToggleMaxWidth(){
    if($('.sidebar').css('left') == '0px'){
        $('.sidebar').css('left', '-15rem');
        $('body').css('margin-left', '0');
        $('.sidebar').removeClass('shadow-lg');
    } else {
        if($('.sidebar').css('display') == 'none'){
            $('.sidebar').css('display', 'block');
        }
        $('.sidebar').css('left', '0');
        $('body').css('margin-left', '15rem');
        $('.sidebar').addClass('shadow-lg');
    }
}
function sidebarToggleMinWidth(){
    if($('.sidebar').css('left') == '0px'){
        $('.sidebar').css('left', '-15rem');
        $('body').css('margin-left', '0');
        $('.sidebar').removeClass('shadow-lg');
        $('.sidebar-full').css('opacity', '0');
        // $('.sidebar-full').css('display', 'none');
        $('.sidebar-full').css('width', '');
        $('.sidebar-full').css('left', '-15rem');
        // $('.sidebar-full').remove();
    } else {
        if($('.sidebar').css('display') == 'none'){
            $('.sidebar').css('display', 'block');
        }
        $('.sidebar').css('left', '0');
        // $('body').css('margin-left', '15rem');
        $('.sidebar').addClass('shadow-lg');
        // $('body').append('');
        // $('.sidebar-full').css('display', 'block')
        $('.sidebar-full').css('opacity', '75%');
        $('.sidebar-full').css('width', 'inhert');
        $('.sidebar-full').css('left', '0');
        
    }
}
$(window).resize(function(){
    if($(window).width() > '750'){
        $('.sidebar-full').css('opacity', '0');
        $('.sidebar-full').css('width', '');
        $('.sidebar-full').css('left', '-15rem');
    }
    else{
        if($('.sidebar').css('left') == '0px'){
            $('.sidebar-full').css('opacity', '75%');
            $('.sidebar-full').css('width', 'inhert');
            $('.sidebar-full').css('left', '0');
        }
    }
})