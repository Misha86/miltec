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
    //$('div.forms').on('submit', 'form#login', function(event){
    //    event.preventDefault();
    //    var form = $(this);
    //    console.log("form submitted!")
    //
    //
    //    $.ajax({
    //        type :  form.attr('method'),
    //        async: true,
    //        url : form.attr('action'),
    //        data : {
    //            email : $('#userid').val(),  // data sent with the post request
    //            password : $('#pw').val()
    //        },
    //        dataType: 'json',
    //
    //        success : function(data) {
    //            console.log('success');            //console.log({{ request.session.color }});
    //            console.log(data);            //console.log({{ request.session.color }});
    //
    //            if(data.form_valid) {
    //                location.href = '/';
    //            } else {
    //                $('.forms').html(data.form_html);
    //                $('div.form-group.has-error').fadeOut(4000);
    //            }
    //            //$('#' + errorId).html("<label id=" + errorId + " class='control-label errorlist'><em>" +
    //            //invalidMessage + "</em></label>");
    //            //console.log(invalidMessage);
    //            //}
    //        },
    //        error: error
    //    });
    //})
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
                //$('#' + errorId).html("<label id=" + errorId + " class='control-label errorlist'><em>" +
                //invalidMessage + "</em></label>");
                //console.log(invalidMessage);
                //}
            },
            error: error
        });
    });

    $.datepicker.setDefaults( $.datepicker.regional[ 'ua' ])
    $("#col3_content .forms #id_date_of_birth").datepicker(
        {changeMonth: true,
            changeYear: true,
            dateFormat: "yy-mm-dd",
            //showOn: "both",
            showWeek: true,
            yearRange: "1920:"

        });
})

