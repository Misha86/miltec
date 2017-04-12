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
});
