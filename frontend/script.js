// Initialize the map
const map = L.map('map').setView([51.505, -.09], 13); // Center the map on a global view

// Add a tile layer (map appearance)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //maxZoom: 15,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Function to fetch data from the backend and plot the migration path
function fetchAndPlotMigrationPath() {

    const URLParams = new URLSearchParams(window.location.search); // search and find the url parameters

    const change_in_temp = URLParams.get('change_in_temp');
    const change_in_wind_speed = URLParams.get('change_in_wind_speed');

    console.log(change_in_temp);
    console.log(change_in_wind_speed)

    if(!change_in_temp || !change_in_wind_speed){
        return; 
    }

  fetch('https://aarons-bird-migration-project.onrender.com/migration_prediction', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          change_in_temp: parseFloat(change_in_temp), // Example payload data
          change_in_wind_speed: parseFloat(change_in_wind_speed)
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

      // array of all the returned migration data
      const migrationData = data.predictions;

      // create an array of all lat and lng points
      var migrationPath = [];

      for(let i=0; i < 90; i++){
        data = migrationData[i].split("/");       // ex: ["1.0", "1.0", "84.03", "34.44"]

        const rawDataDiv = document.getElementById("raw-data");
        rawDataDiv.textContent = data;

        // grab the month and day
        var day = parseInt(data[1], 10).toString();
        var month = parseInt(data[0], 10).toString();

        let point = [parseFloat(data[3]), parseFloat(data[2])]; // create the point for the polyine
        migrationPath.push(point);                              // add the point to the polyline

        var marker = L.marker([parseFloat(data[3]), parseFloat(data[2])]).addTo(map);
        marker.bindPopup(month + "/" + day).openPopup();
      }

      // Plot the migration path on the map
      const polyline = L.polyline(migrationPath, {color: 'blue'}).addTo(map);

      // Zoom the map to fit the polyline
      map.fitBounds(polyline.getBounds());
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

// Call the function to fetch data and plot the migration path
fetchAndPlotMigrationPath();
