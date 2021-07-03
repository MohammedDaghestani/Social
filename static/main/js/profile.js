$(document).ready(function(){
    toggleHomeLink();
    // $('#insert>li>a').click(function(){
    //     $('#insert>li>a').removeClass('active , text-light');
    //     $(this).addClass('active , text-light');
    // });
});
$(window).resize(function(){
    toggleHomeLink();
});
function toggleHomeLink(){
    var home = $('#toggleItem')
    if($(window).width() <= 767.98){
        $('#toggleItem>a').removeClass('active'); 
        $('#insert').prepend(home);
    }
    else{
        $('#toggleItem>a').addClass('active');
        $('#nav').prepend(home);
    }
};