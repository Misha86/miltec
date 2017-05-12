$(function () {

    var cartAdd = function (event){
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
                    $('#topnav > span > a.cart_url > b').html(data.total_price + ' EUR*');
                } else {
                    console.log(data.form_valid)
                }
                if(data.html_messages){
                    addDjangoMessage(data.html_messages, '#messages', 7000);
                }
            },
            error: error
        });
    };

    var cartRemove = function (event){
        event.preventDefault();
        var link = $(this);
        var dataProduct = link.attr('data-product');
        $.ajax({
            url : link.attr('href'),
            success : function(data) {
                var cartTable = $('.cart');
                if(data.total_price) {
                    cartTable.find("tr[id='" + dataProduct + "']").remove();
                    cartTable.find("td[id='total_price']").text(data.total_price + ' EUR*');
                } else {
                    $('#cart-details').html(data.empty_cart)
                }
            },
            error: error
        });
    };

    $('#main').on('submit', 'form.cart-form', cartAdd);

    $('#cart-details').on('click', 'a.cart-remove', cartRemove);

});
