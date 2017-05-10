var map;
var service;
var infowindow;

function addMarker(place) {
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        icon: {
            url: "/static/img/np-marker.png",
            anchor: new google.maps.Point(10, 10),
            scaledSize: new google.maps.Size(20, 34)
        },
        title: place.name + ' \n' + place.vicinity
    });

    // marker for new post
    google.maps.event.addListener(marker, 'click', function() {
        service.getDetails({
            placeId: place.place_id
        }, function(result, status) {
            if (status !== google.maps.places.PlacesServiceStatus.OK) {
                console.error(status);
                return;
            }

            $('input#id_address').val(result.name + ' ' + result.formatted_address);

            map.setZoom(15);
            map.setCenter(marker.getPosition());

            infowindow.setContent('<div><strong>' + result.name + '</strong><br>' +
            '<br>' + result.formatted_address + '</div>');
            infowindow.open(map, marker);
        });
    });
}

function callback(places, status) {
    //console.log(places);
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        for(var i=0; i < places.length; i++){
            addMarker(places[i]);
        }
    }
}

function performSearch (){
    var request = {
        bounds: map.getBounds(),
        name: 'новая почта'
    };
    service.nearbySearch(request, callback);
}

function initialise (location){
    //console.log(location);
    var myLatLng;
    if(location.code == 1){
        myLatLng = {lat: 50.626867, lng: 26.2052116};
    } else {
        myLatLng = {lat: location.coords.latitude, lng: location.coords.longitude};
    }

    var mapOptions = {
        center: myLatLng,
        zoom: 12
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'Моя локация'
    });

    // add close buttton
    var closeButton = document.createElement('div');
    closeButton.text = 'Close';
    $(closeButton).addClass('close-map');
    $(closeButton).click(function(){
        $('#map').hide();
        $('body').scrollTop(0)
    });

    map.controls[google.maps.ControlPosition.RIGHT_TOP].push(closeButton);

    // marker my location
    marker.addListener('click', function() {
        map.setZoom(15);
        //console.log(this.title);
        map.setCenter(this.getPosition());
    });

    infowindow = new google.maps.InfoWindow();
    service = new google.maps.places.PlacesService(map);

    google.maps.event.addListener(map, 'bounds_changed', performSearch);
}

$(function(){

    $("input#id_address").click(function() {

        var map = $('#map');
        map.show();

        navigator.geolocation.getCurrentPosition(initialise, initialise);

        $('html, body').animate({
            scrollTop: map.offset().top - 20
        }, 1000);

    });
})