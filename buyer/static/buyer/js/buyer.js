// Acquiring the token is straightforward using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var color = getCookie('color');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


//Submit post on submit
$(function () {

    $('div.forms').on('submit', 'form#login', function(event){
        event.preventDefault();
        var form = $(this);

        $.ajax({
            type :  form.attr('method'),
            async: true,
            url : form.attr('action'),
            data : form.serialize(),
            dataType: 'json',

            success : function(data) {
                if(data.form_valid) {
                    location.href = data.redirect_path;
                } else {
                    $('.forms').html(data.form_html);
                    $('div.form-group.has-error').fadeOut(4000);
                }
            },
            error: error
        });
    });

    var loadForm = function (event) {
        event.preventDefault();
        $.ajax({
            url: this.href,
            dataType: 'json',
            success: function (data) {
                $('.modal').modal();
                $('.modal-content').html(data.delete_form);
            },
            error : error
        });
    };

    var deleteForm = function (event) {
        event.preventDefault();
        var form = $(event.target);
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',

            success: function (data) {
                if(data.is_data){
                    $('.modal').modal('hide');
                    console.log('success');
                    location.pathname = data.redirect_path;
                }
            },
            error : error
        });
    };

    var selectorBody = $("body");

    selectorBody.on('click', '.delete-ajax', loadForm);
    selectorBody.on('submit', '.js-profile-delete-form', deleteForm)
});

