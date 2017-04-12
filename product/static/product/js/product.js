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
    });

//$('#query').autocomplete({
//    autoFocus: true,
//    classes: {
//        "ui-autocomplete": "my-autocomplete"
//    },
//    minLength: 1,
//
//    source: function(request, response){
//        // организуем кроссдоменный запрос
//        $.ajax({
//            url: '/product/search/',
//            dataType: "json",
//            // параметры запроса, передаваемые на сервер (последний - подстрока для поиска):
//            data:{
//                //featureClass: "P",
//                //style: "full",
//                //maxRows: 3,    // показать первые 12 результатов
//                q: request.term
//            },
//            // обработка успешного выполнения запроса
//            success: function(data){
//                console.log(data.json_query)
//
//                // приведем полученные данные к необходимому формату и передадим в предоставленную функцию response
//                response($.map(data.json_query, function(item){
//                    return{
//                        //label: item.name + (item.adminName1 ? ", " + item.adminName1 : "") + ", " + item.countryName,
//                        value: item
//                    }
//                }));
//            }
//        });
//    }
//});

// search articles when push submit button
    $("#searchForm").on('submit', function(event){
        event.preventDefault();
        var form = $(this);
        console.log('wef')
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
    });

    $("#col3_content > form > div > dl > dd.image > a[rel^='prettyPhoto']").prettyPhoto({
        theme: 'pp_default',	/* pp_default / light_rounded / dark_rounded / light_square / dark_square / facebook */
        hideflash: false, /* Hides all the flash object on a page, set to TRUE if flash appears over prettyPhoto */
        social_tools: false, /* html or false to disable */
        deeplinking: false, /* Allow prettyPhoto to update the url to enable deeplinking. */
        ie6_fallback: true,
        overlay_gallery: false /* If set to true, a gallery will overlay the fullscreen image on mouse over */,
        iframe_markup:'<div class="iOSscroll" style="width:{width}px;height:{height}px;"><iframe src ="{path}" width="{width}" height="{height}" frameborder="no"></iframe></div>' /* Bugfix for iOS Touch devices to be able to scroll */
    });

});
