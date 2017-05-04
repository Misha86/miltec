var successSearch = function(data) {

    var content = $("#col3_content");

    if (data.is_data) {

        content.html(data.html_items);

    } else {
        console.log(data.is_data);
    }
    //console.log(data);
};


$(function () {

    // jquery ajax live search
    $('#searchForm').keyup(function (event) {
        event.preventDefault();
        var form = $(this);
        var locHref = location.pathname;
        $.ajax({
            async: true,
            url: form.attr("action"),
            type: form.attr("method"),
            data: {
                q: $("#query").val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: 'json',

            success: successSearch,
            error: error
        });

        window.history.pushState({href: locHref}, form.attr("action"), locHref);
    });

    // search articles when push submit button
    $("#searchForm").on('submit', function(event){
        event.preventDefault();
        var form = $(this);
        var locHref = location.pathname;
        $.ajax({
            async: true,
            url: form.attr("action"),
            type: form.attr("method"),
            data: {
                q : $("#query").val()
            },
            dataType: 'json',

            success: successSearch,

            error : error
        });

        window.history.pushState({href: locHref}, form.attr("action"), locHref);

    });
});
