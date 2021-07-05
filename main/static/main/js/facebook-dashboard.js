var pages = document.getElementById('page_id');
pages.onchange = function() {change_page()};
function change_page() {
    $.post('/accounts/facebook/', {'page_id': pages.value})
};
