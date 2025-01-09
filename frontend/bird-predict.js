const dropZone = document.getElementById('imageDropZone');
const fileInput = document.getElementById('fileInput');

// highlight when a file is hovering over
dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragover');
});

// remove highlight when file leaves
dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

// handle the dropped in file
dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragover');

    const files = event.dataTransfer.files;
    if(files.length){
        // handle file with whatever function built
        uploadImage(files[0]);
    }
});

// Handle the file by sending to back-end server
function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('https://aarons-bird-migration-project.onrender.com/bird_detection', {
        method: 'POST',
        // Remove the headers to allow the browser to set 'Content-Type' automatically
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            alert(`Response isn't ok: ${response.status}`);
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const result = `Bird Species Prediction: ${data.class}, Confidence: ${data.confidence}`;
            const resultsDiv = document.getElementById("results");
            resultsDiv.textContent = result;
        }
    })
    .catch(error => {
        alert(error);
    });
}
