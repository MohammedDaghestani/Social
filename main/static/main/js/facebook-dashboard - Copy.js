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
// $('#loadMore').on('click', function () {
//     // xhttp = new XMLHttpRequest();
//     // xhttp.onload = function () {
//     //     $('#loadMore').before(this.responseText);
//     //     oldPosts = sessionStorage.getItem('posts');
//     //     console.log('old = ' + oldPosts);
//     //     if (oldPosts != null) {
//     //         newPosts = oldPosts + this.responseText;
//     //         // console.log(newPosts);
//     //         sessionStorage.setItem('posts', newPosts);
//     //         // alert('done')
//     //     }
//     //     else{
//     //         // console.log(this.responseText);
//     //         sessionStorage.setItem('posts', this.responseText);
//     //     }
//     // }
//     // xhttp.open('GET', 'more-posts', true);
//     // xhttp.send();
//     // document.cookie = "posts=" + this.value;
//     // location.reload();
    
//     $.get('more-posts', function (posts) {
//         $('#loadMore').before(posts);
//     })
// })
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


list = $('.list-group').on('scroll', function () {
    if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight && document.getElementsByClassName('list-group-item').length != 0){
        if (document.getElementById('no-more') == null) {
            add_spinner('.list-group');
            $.get('more-posts', function (posts) {
                remove_spinner();
                if(posts != 'None'){
                    $('.list-group').append(posts);
                } else {
                    var no_more = document.getElementById('no-more');
                    if (no_more == null) {
                    $('.list-group').append('<div class="text-center form-text p-3" id="no-more">No more posts to show</div>');
                    }
                }
            })
        }
    }
})
$('.posts-buttons').on('click', function () {
    $('.posts-buttons').removeClass('buttons-active');
    $(this).addClass('buttons-active');
})

$('#scheduled').on('click', function () {
    $('.lifetime').css('display', 'none');
    $('.list-group-item').remove();
    $('#no-more').remove();
    add_spinner('.list-group');
    $.get('scheduled-posts' , function(post){
        $('#no-more').remove();
        remove_spinner();
        if (post != 'None') {
            $('.list-group').append(post);
        } else {
            $('.list-group').append('<div class="text-center form-text p-1" id="no-more"><br>No results to show</div>');
        }
    })    
})

$("#lifetime").on('change', function(){
    $('.list-group-item').remove();
    $('#no-more').remove();
    add_spinner('.list-group');
    $.get('posts/' + this.value, function(posts){
        $('.list-group-item').remove();
        $('#no-more').remove();        
        remove_spinner();
        if(posts != 'noPosts'){
            $('.list-group').append(posts);
        } else {
            $('.list-group').append('<div class="text-center form-text p-1" id="no-more"><br>No posts to show</div>');
        }
    })
})


$('#published').on('click', function(){
    $('.lifetime').css('display', 'block');
    $('.list-group-item').remove();
    $('#no-more').remove();
    add_spinner('.list-group');
    $.get('more-posts', function (posts) {
        $('.list-group-item').remove();
        $('#no-more').remove();        
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
})


$('#search').on('input propertychange ',function(){
    var valu = this.value;
    $('.list-group-item').remove();
    $('#no-more').remove();
    add_spinner('.list-group');
    if(valu != ''){
        var path = 'search-post/' + valu
        $.get(path , function(post){
            $('#no-more').remove();
            remove_spinner();
            if(post != 'noResults'){
                $('.list-group').append(post);
            } else if(post == 'noResults') {
                $('.list-group').append('<div class="text-center form-text p-1" id="no-more">No results to show</div>');
            } else {
                $('.list-group').append('<div class="text-center form-text p-1" id="no-more">Page Error</div>');
            }
        })  
    } else {
        $.get('more-posts', function (posts) {
            $('.list-group-item').remove();
            $('#no-more').remove();        
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
})