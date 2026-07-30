// static/js/dashboard.js

function getLocation(){

    if(navigator.geolocation){

        navigator.geolocation.getCurrentPosition(showPosition, showError);

    }
    else{

        alert("Geolocation is not supported.");

    }

}

function showPosition(position){

    let lat = position.coords.latitude;
    let lon = position.coords.longitude;

    const selectedUnit =
        new URLSearchParams(window.location.search).get("unit") || "metric";

    window.location.href =
        `/current-location/?lat=${lat}&lon=${lon}&unit=${selectedUnit}`;

}

function showError(error){

    switch(error.code){

        case error.PERMISSION_DENIED:
            alert("Location permission denied.");
            break;

        case error.POSITION_UNAVAILABLE:
            alert("Location unavailable.");
            break;

        case error.TIMEOUT:
            alert("Location timeout.");
            break;

        default:
            alert("Unable to get location.");

    }

}