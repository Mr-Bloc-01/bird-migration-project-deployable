
// access the input-form element and add a lister
document.getElementById('input-form').addEventListener('submit', function(event) {

    event.preventDefault(); // prevent the page from refreshing and allow to be redirected to the map-page.html

    // create variables to store user inputted values
    const temperature = parseFloat(document.getElementById('temperature').value);
    const wind_speed = parseFloat(document.getElementById('wind_speed').value);

    // perform redirect
    window.location.replace(`/map-page.html?change_in_temp=${temperature}&change_in_wind_speed=${wind_speed}`);
});