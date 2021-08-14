// Elements
const words_input       = document.getElementById('words-input');
const words_container   = document.getElementById('words-container');
const replies_container = document.getElementById('replies-container');
const btn_add_reply     = document.getElementById('btn-add-reply');
const rep_input         = document.getElementById('reply');
const rep_privately_input = document.getElementById('reply-privately')
const form_add_reply    = document.getElementById('form-add-reply');
var words               = '';
let reply_for_delete = ''
//Events
// words_input.addEventListener('change', add_word);
// btn_add_reply.addEventListener('click', add_reply);

//Functions
$(document).ready(function () {
    delete_btn_events();
    edit_btn_events();
})



$(words_input).on('change', function() {
    add_word();
})
$(words_input).on('keypress', function (event) {
    if(event.keyCode === 13 || event.keyCode === 32){
        event.preventDefault();
        add_word();
    }
})
$(rep_input).keypress(function (event) {
    if(event.keyCode === 13){
        event.preventDefault();
        rep_privately_input.focus();
    }
})
$(rep_privately_input).keypress(function (event) {
    if(event.keyCode === 13){
        event.preventDefault();
    }
})
function add_word() {
    // event.preventDefault();
    if(words_input.value != ''){
        $(words_container).append(make_word_div(words_input.value));
    }
    words_input.value = '';
    add_event_to_word();
    // return false;
}
function make_word_div(word) {
    let div = '<div class="word">' + word + '</div>';
    return div;
}

function make_reply_word_div(word) {
    if (word.trim() != '') {
        let div = '<div class="reply-word">' + word + '</div>';
        return div;
    }
    else{
        return ''
    }
}


function remove_word() {
    $(this).remove();
}
function add_event_to_word() {
    words = document.querySelectorAll('.word');
    words.forEach(word => {
        word.addEventListener('click', remove_word);
    });
    
}

// function add_reply() {
//     ws_divs = words_container.getElementsByClassName('word');
//     ws = [];
//     for(var i=0 ; i < ws_divs.length; i ++){
//         if (ws_divs[i].innerHTML.trim() != '') {
//             ws.push(ws_divs[i].innerHTML);
//         }
//     }
//     $(replies_container).append(make_reply(ws, rep_input.value, rep_privately_input.value));
//     $('.word').remove();
//     rep_input.value = '';
//     rep_privately_input.value = '';
//     words_input.focus();
// }

function delete_btn_events() {
    $('.delete').hover(delete_btn_hover);
    $('.delete').mouseleave(delete_btn_mouseleave);
    $('.delete').click(delete_btn_click);
}

function edit_btn_events() {
    $('.edit').click(edit_btn_click);        
}

function edit_btn_click() {
    let card_bodies = $(this).parent().parent().parent().find('.card-body');
    let wrd_container = $(card_bodies[0]).find('#reply-words-container');
    let wds_div = $(wrd_container).find('.reply-word');
    $(words_container).empty();
    for (let i = 0; i < wds_div.length; i++) {
        let wd = $.trim(wds_div[i].innerHTML);
        if(wd != ''){
            $(words_container).append(make_word_div(wd));
        }
    }
    let r_id = document.getElementById('reply-id');
    r_id.value = $(this).parent().parent().parent().attr('id');
    rep_input.value = $(card_bodies[1]).find('.reply-with')[0].innerText.trim();
    if($(card_bodies[1]).find('.reply-privately')[0] != undefined){
        rep_privately_input.value = $(card_bodies[1]).find('.reply-privately')[0].innerText.trim();
    }
    $(this).parent().parent().parent().remove();
    add_event_to_word();
    words_input.focus();
}


// function make_reply(words, reply, private_reply) {
//     let words_div = '' 
//     words.forEach(word => {
//         if(word !=''){
//             console.log('word = '+word)
//             words_div += make_reply_word_div(word);
//         }
//     });
//     let divs = '<div class="card"><div class="card-body"><div id="reply-words-container">' + words_div + '</div></div><div class="card-body card-body-reply"><div class="reply-with">Comment: ' + reply + '</div><div class="reply-privately">Private: ' + private_reply + '</div><button class="btn btn-outline-primary" ></button></div></div>'
//     return divs;
// }
$(form_add_reply).on('submit', function (event) {
    $(btn_add_reply).addClass('disabled');
    event.preventDefault();
    let r_id = document.getElementById('reply-id').value; 
    // console.log('r_id value = '+ r_id)
    wds_divs = words_container.getElementsByClassName('word');
    wds = '';
    if(r_id != ''){
        let frm_data = {
            'reply_id': r_id
        }
        var xhr = $.ajax({
            url: '/accounts/facebook/post/reply', 
            method: 'GET',
            data: frm_data
        }) 
    }
    if(wds_divs.length != 0){
        for(var i =0; i< wds_divs.length; i++){
            if(i!=0) wds += ' ';
            wds+= wds_divs[i].innerHTML;
        }
    }
    
    rep = rep_input.value;
    private_rep = rep_privately_input.value;
    post_id = document.getElementById('post_id');
    csrf = document.getElementsByName('csrfmiddlewaretoken');
    
    let form_data = {
        'post_id': post_id.value,
        'words': wds,
        'reply': rep,
        'private_reply': private_rep
    }
    // console.log(form_data);
    var xhr = $.ajax({
        headers: {'X-CSRFToken': csrf[0].value},
        url: '/accounts/facebook/post/reply', 
        method: 'POST',
        data: form_data
    }) .done(function (response) {
        $(replies_container).append(response);
        $('#error-add-reply-alert').remove();
        $('#recommendations').remove();
        $('.word').remove();
        rep_input.value = '';
        rep_privately_input.value = '';
        r_id.value = ''
        words_input.focus();  
        edit_btn_events();
        delete_btn_events();
    }) .fail(function () {
        let alert = '<div id="error-add-reply-alert" class="alert alert-danger alert-dismissible fade show" role="alert"><strong>Error</strong> Please check your internet connection.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
        if(document.getElementsByClassName('alert').length == 0){
            $('#add_reply').before(alert)
        }
    })
    $(btn_add_reply).removeClass('disabled');
    
})

function delete_btn_hover() {
    parent = $(this).parent()
    $(parent).parent().parent().addClass('border-left-red')
}
function delete_btn_mouseleave() {
    parent = $(this).parent()

    // $(parent).parent().parent().addClass('border-left-blue')
    $(parent).parent().parent().removeClass('border-left-red')
}


function delete_btn_click() {
    reply_for_delete = $(this).parent().parent().parent().attr('id');
}
$('#delete-reply').click(function () {
    form_data = {
        'reply_id': reply_for_delete
    }
    var xhr = $.ajax({
        url: '/accounts/facebook/post/reply', 
        method: 'GET',
        data: form_data
    }) .done(function (response) {
        if(response == 'done'){
            r = document.getElementById(reply_for_delete);
            $(r).remove();
        }
    })
})
