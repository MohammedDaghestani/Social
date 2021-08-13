// pages.onchange = function() {change_page()};


var e = document.getElementById('page_id').value;
var csrf = document.getElementsByName('csrfmiddlewaretoken').value;
$('#page_id').on('change', function() {
    document.cookie = "page_id=" + this.value;
    console.log(document.cookie);
    location.reload();
});