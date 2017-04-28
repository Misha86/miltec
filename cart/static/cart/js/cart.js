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
            },
            error: error
        });
    };

    $('#main').on('submit', 'form.cart-form', cartAdd);

});
