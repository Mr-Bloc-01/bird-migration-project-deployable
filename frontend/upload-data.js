window.addEventListener("DOMContentLoaded", async () => {
  let button = document.getElementById("submit-button");
  button.addEventListener("click", async () => {
    species_input = document.getElementById("bird-species");
    temperature_input = document.getElementById("temperature");
    wind_speed = document.getElementById("wind-speed");
    wind_direction = document.getElementById("wind-direction");

    uploadData( // update the database with the user inputted data
      species_input.data,
      temperature_input.data,
      wind_speed.data,
      wind_direction.data
    );
  });

  });
  

  window.onload = async function () {
    async function requestOrientationPermission() {
      console.log("called request orientation permission");
      if (typeof DeviceOrientationEvent.requestOrientationPermission === "function") {
        try {
          const permission = await DeviceOrientationEvent.requestOrientationPermission();
          if (permission === "granted") {
            console.log("Device orientation permission granted.");
            window.addEventListener("deviceorientationabsolute", handleOrientationUpdate);
          } else {
            console.log("Device orientation permission not granted.");
          }
        } catch (error) {
          console.error("error!", error);
        }
      }
    }

    // request the orientation permission and draw the compass
    requestOrientationPermission();
  };

// requesting geolocation using the geolocation api
function getGeoLocation() {
  try {
    const position = navigator.geolocation.getCurrentPosition();  // get their current position
    const coords = position['coords'];  // extract the coordinates
    return coords;
  } catch (error) {
    console.error("Geolocation Error", error);
  }
}

function uploadData(species, temperature, wind_speed, direction) {

  const coords = getGeoLocation || {coords: {lattitude: 0, longitude: 0}};
  
  fetch('https://aarons-bird-migration-project.onrender.com/upload-data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        species: species,
        temperature: temperature,
        wind_speed: wind_speed,
        direction: direction,
        coords: coords
    }),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON response
  })
  .then(data => {
      console.log('Success:', data);
      alert("successfully uploaded your data, thank you! :)");
  })
  .catch(error => {
      console.error('Error:', error);
  });
}