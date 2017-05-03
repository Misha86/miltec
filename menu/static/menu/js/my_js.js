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


    var ajaxForProducts =  function (urlDjango) {

        $.ajax({
            url: urlDjango,
            type: 'get',
            dataType: 'json',

            success: function (data) {

                var content = $("#col3");

                if (data.is_data) {

                    content.html(data.html_items);

                } else {

                    console.log('false');
                }
            },
            error : error
        });

    };


    var items =  function (event) {
        event.preventDefault();
        var category = $(event.currentTarget);
        var urlDjango = category.attr('href');
        console.log(category.attr('href'));

        ajaxForProducts(urlDjango);

        window.history.pushState({href: urlDjango}, category.attr('id'), urlDjango);

    };


    window.addEventListener('popstate', function(event){
        if(event.state){
             ajaxForProducts(event.state.href);
        } else {
            location.href = '/'
        }
    });


    var mainContent = $("#main");

    $(".full.content").on('click', 'a', items);
    $(".category").on('click', 'a', items);

    // show items in category from accordion
    mainContent.on('click', '#col3_content tr td a', items);

    $(".indentLevel_0").on('click', 'a', items);
    $(".indentLevel_1").on('click', 'a', items);

    // url for details product
    //$("#col3").on('click', 'div#col3_content div.products div.product-row.hproduct a', items);
    mainContent.on('click', '#col3_content .products .subcl div.product-row.hproduct a', items);

    // ajax pagination
    mainContent.on('click', "#col3_content .pagination a", items);
    mainContent.on('click', ".toolBar.clearfix a", items);

    // breadcrumb
    mainContent.on('click', "#col3_content .breadcrumbBar .breadcrumbs li.elseCrumb a", items);

    //// product details 'next' and 'back'
    mainContent.on('click', ".bottomToolBar .tools.float_right a", items);

});
