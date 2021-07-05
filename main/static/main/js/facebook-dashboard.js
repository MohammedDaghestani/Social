// var pages = document.getElementById('#page_id');
// pages.onchange = function() {change_page()};


$('#page_id').change(function() {
    $.post('/accounts/facebook/', {'page_id': pages.value})    
})