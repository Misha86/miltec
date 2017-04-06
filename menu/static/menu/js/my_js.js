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


var error = function(xhr, errmsg, err) {
    $('#result').html("<div class='container' data-alert><h1>Oops! We have encountered an error: " + xhr.status + errmsg +
    "</h1><a href='#' class='close'>&times;</a></div>"); // add the error to the dom
    alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg )
    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
};


$(function () {
    $('.hlist li').each(function () {
        var location = window.location.pathname;
        var link = $(this).find('a').attr('href');
        if(location == link) {
            $(this).addClass('selected');
        }
    });
});



var breadcrumb = function(){
    var breadcrumbs = $('#col3_content > form > div.breadcrumbBar.clearfix > ul')
    var acordionSel = $(".ui-accordion-header-active");
    var itemOne = $(".indentLevel_0.selected");
    var itemTwo = $(".indentLevel_1.selected");
    var crumb = [acordionSel, itemOne, itemTwo];
    for(var i=0; i < crumb.length; i++){
        if(crumb[i].text() != ''){
            breadcrumbs.append("<li> » <a href='#'>" + crumb[i].text() +"</a></li>")
        }
    }
    console.log($(breadcrumbs));
};


$(function () {
    $( ".accordion" ).accordion({
        beforeActivate:function(event, ui){
            $(ui.oldPanel).find('li.selected').removeClass('selected');
            $(ui.oldPanel).find('li.indentLevel_1').slideUp();
        },
        heightStyle: "content",
        header: "h5",
        collapsible: true,
        active: false,
        classes: {
            "ui-accordion-header-collapsed": "selected"
        }
    });

    $('.widget').on('click', '.indentLevel_0', function(event){
        event.preventDefault();
        var targetData = $(event.currentTarget);
        var subCad = targetData.nextUntil('li.indentLevel_0');

        $('.indentLevel_0').each(function () {
            if ($(this).hasClass("selected") && $(this).attr('id') != targetData.attr('id')){
                $(this).removeClass("selected");
                $(this).nextUntil('li.indentLevel_0').removeClass("selected");
                $(this).nextAll('li.indentLevel_1').slideUp();
            }
        });
        //console.log($(this) != targetData)
        targetData.toggleClass("selected");
        subCad.removeClass("selected")
        subCad.slideToggle();

    });

    $('.indentLevel_1').click(function(event){
        event.preventDefault();

        $('.indentLevel_1').each(function () {
            if ($(this).hasClass("selected")) {
                $(this).removeClass("selected");
            }
        });

        //console.log($(this) != targetData)
        $(event.currentTarget).toggleClass("selected");

    });


    var items =  function (event) {
        event.preventDefault();
        var category = $(event.target);
        console.log(category.attr('href'));
        $.ajax({
            url: category.attr('href'),
            type: 'get',

            success: function (data) {

                var content = $("#col3_content");

                if (data.is_data) {

                    content.html(data.html_items);
                    breadcrumb()

                } else {
                    content.html('');
                    console.log(data.is_data);
                }
            },
            error : error
        });
    };

    $(".full.content").on('click', 'a', items);
    $(".category").on('click', items);

    $("#main").on('click', '#col3_content h2.uppercase a', items);

    $(".indentLevel_0").on('click', 'a', items);
    $(".indentLevel_1").on('click', 'a', items);

});