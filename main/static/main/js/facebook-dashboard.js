$('#page_id').on('change', function() {
    document.cookie = "page_id=" + this.value;
    location.reload();
});
$(document).ready(function () {
    if($(window).width() <= '750'){
        $('.stik').css('display', 'none');
    } else {
        $('.stik').css('display', 'block');
    }

    if(window.performance.navigation.type == 2){
        location.reload();
    }
     
})
$(window).resize(function () {
    if($(window).width() <= '750'){
        $('.stik').css('display', 'none');
    } else {
        $('.stik').css('display', 'block');
    }
})

const scheduled_posts   = document.querySelector('#scheduled');
const list_group        = document.querySelector('.list-group');
const posts_buttons     = document.querySelectorAll('.posts-buttons');
const published_posts   = document.getElementById('published');
const search            = document.getElementById('search');
const lifetime          = document.getElementById('lifetime'); 
var xhr = null;

//URLs
const url_more_posts        = 'more-posts';
const url_scheduled_posts   = 'scheduled-posts';
const url_published_posts   = 'published-posts';
const url_search_post       = 'search-post/'
const url_lifetime_posts    = 'posts/';

//Elements
const element_no_more_posts = '<div class="text-center form-text p-3" id="no-more">No more posts to show</div>'

//Events 
list_group.addEventListener('scroll', list_group_more_posts);
scheduled_posts.addEventListener('click', scheduled_posts_button);
published_posts.addEventListener('click', published_posts_button);
search.addEventListener('propertychange', search_posts_input);
search.addEventListener('input', onlyNumbers);
search.addEventListener('input', search_posts_input);
lifetime.addEventListener('change', lifetime_select);

//Functions
function onlyNumbers() {
    $(this).val($(this).val().replace(/[^0-9]/g, ''));    
}

function posts_buttons_toggle(button) {
    $(posts_buttons).removeClass('buttons-active');
    $(button).addClass('buttons-active');
}

// function removeEvents(){
//     published_posts.removeEventListener('click', published_posts_button);
//     scheduled_posts.removeEventListener('click', scheduled_posts_button);
//     list_group.removeEventListener('scroll', list_group_more_posts);
// }
// function addEvents() {
//     list_group.addEventListener('scroll', list_group_more_posts);
//     scheduled_posts.addEventListener('click', scheduled_posts_button);
//     published_posts.addEventListener('click', published_posts_button);        
// }

function add_spinner(element) {
    var spinner = '<div class="d-flex justify-content-center spinner"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>'
    var spin = document.getElementsByClassName('spinner');
    if(spin.length == 0){
        $(element).append(spinner);
    }
}

function remove_spinner(){
    $('.spinner').remove();
}

function remove_list_group_elements() {
    $('.list-group-item').remove();
    $('#no-more').remove();
}

$.ajaxSetup({
    method: 'GET',
    dataType: "html",
    context: $('.list-group'),
    beforeSend: function () {
        if(xhr){
            xhr.abort();
        }
    }
}) 

function  list_group_more_posts() {
    if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight && document.getElementsByClassName('list-group-item').length != 0){
        if (document.getElementById('no-more') == null) {
            list_group.removeEventListener('scroll', list_group_more_posts);
            add_spinner(this);
            xhr = $.ajax({
                url: url_more_posts,
            }).done(function (posts) {
                remove_spinner();
                if(posts != 'None'){
                    $(this).append(posts);
                } else {
                    var no_more = document.getElementById('no-more');
                    if (no_more == null) {
                    $(this).append(element_no_more_posts);
                    }
                }
                list_group.addEventListener('scroll', list_group_more_posts);
            })
        }
    }
}

function scheduled_posts_button() {
    empty_search();
    $(lifetime).css('display', 'none');
    posts_buttons_toggle(this);
    remove_list_group_elements();
    add_spinner('.list-group');
    xhr = $.ajax({
        url: url_scheduled_posts,
    }) .done(function (post) {
        remove_spinner();
        remove_list_group_elements();
        if (post != 'None') {
            $('.list-group').append(post);
        } else {
            $('.list-group').append('<div class="text-center form-text p-1" id="no-more"><br>No results to show</div>');
        }
    })
}

function published_posts_button(){
    empty_search();
    empty_lifetime();
    $(lifetime).css('display', 'block');
    posts_buttons_toggle(this);
    remove_list_group_elements();
    add_spinner('.list-group');
    xhr = $.ajax({
        url: url_published_posts,
    }).done(function (posts) {
        remove_spinner();
        remove_list_group_elements();
        if(posts != 'None'){
            $('.list-group').append(posts);
        } else {
            var no_more = document.getElementById('no-more');
            if (no_more == null) {
                $('.list-group').append('<div class="text-center form-text p-1" id="no-more">No more posts to show</div>');
            }
        }
        list_group.addEventListener('scroll', list_group_more_posts);
    })
}


function search_posts_input(){
    empty_lifetime();
    var valu = this.value;
    remove_list_group_elements();
    add_spinner('.list-group');
    if(valu != ''){
        var path = url_search_post + valu
        xhr = $.ajax({
            url: path,
        }) .done(function (post) {
            remove_list_group_elements();
            remove_spinner();
            if(post != 'noResults'){
                if (post.startsWith('1')) {
                    posts_buttons_toggle('#scheduled');
                    $('.list-group').append(post.slice(1));
                } else {
                    posts_buttons_toggle('#published');
                    $('.list-group').append(post);
                }
            } else if(post == 'noResults') {
                $('.list-group').append('<div class="text-center form-text p-1" id="no-more">No results to show</div>');
            } else {
                $('.list-group').append('<div class="text-center form-text p-1" id="no-more">Page Error</div>');
            }
        })
    } else {
        xhr = $.ajax({
            url:url_published_posts,
        }) .done(function (posts) {
            posts_buttons_toggle('#published');
            remove_list_group_elements();
            remove_spinner();
            if(posts != 'None'){
                $('.list-group').append(posts);
            } else {
                var no_more = document.getElementById('no-more');
                if (no_more == null) {
                    $('.list-group').append('<div class="text-center form-text p-1" id="no-more">No more posts to show</div>');
                }
            }
        })
    }
}
function lifetime_select() {
    empty_search();
    remove_list_group_elements();
    add_spinner('.list-group');
    path = url_lifetime_posts + lifetime.value
    xhr = $.ajax({
        url: path, 
    }) .done(function (posts) {
        remove_list_group_elements();
        remove_spinner();
        if(posts != 'noPosts'){
            $('.list-group').append(posts);
        } else {
            $('.list-group').append('<div class="text-center form-text p-1" id="no-more"><br>No posts to show</div>');
        }
        if(lifetime.value != 'lifetime'){
            list_group.removeEventListener('scroll', list_group_more_posts);
        } else {
            list_group.addEventListener('scroll', list_group_more_posts);
        }
    })
}

function empty_lifetime(){
    lifetime.removeEventListener('change', lifetime_select);
    lifetime.value = 'lifetime';
    lifetime.addEventListener('change', lifetime_select);
}
function empty_search() {
    search.removeEventListener('propertychange', search_posts_input);
    search.removeEventListener('input', search_posts_input);
    search.value = '';
    search.addEventListener('input', search_posts_input);
    search.addEventListener('propertychange', search_posts_input);

}
