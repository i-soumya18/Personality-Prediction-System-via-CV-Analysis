function uploadResume() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('file', file);

    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    let width = 1; // Start at 1% to show progress immediately
    const interval = setInterval(frame, 30);

    function frame() {
        if (width >= 99) {
            clearInterval(interval);
            width = 100; // Ensure the progress bar reaches 100%
            progressBar.style.width = width + '%';
            progressText.innerHTML = 'Almost there...'; // Update text just before completion
            setTimeout(() => initiateFetch(formData), 300); // Wait 300ms before initiating fetch
        } else {
            width++;
            progressBar.style.width = width + '%';
        }
    }

    function initiateFetch(formData) {
        // Display a loading indicator while waiting for the response
        progressText.innerHTML = 'Loading...';

        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            clearInterval(interval); // Stop the progress bar when the response is received
            progressBar.style.width = '100%'; // Ensure the progress bar reaches 100% on completion
            progressText.innerHTML = 'Data processed'; // Update text upon completion
            return response.text();
        })
        .then(data => {
            // Update the result section with the extracted data
            document.getElementById('result').innerHTML = data;
        })
        .catch(error => {
            // Display an error message in case of failure
            progressText.innerHTML = 'An error occurred. Please try again.';
            console.error('Error:', error);
            clearInterval(interval); // Stop the progress bar in case of an error
        });
    }
}