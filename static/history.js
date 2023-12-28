// In history.js
document.addEventListener('DOMContentLoaded', function() {
    fetch('/history')
        .then(response => response.json())
        .then(data => displayHistory(data))
        .catch(error => console.error('Error fetching history:', error));
});

function displayHistory(data) {
    const historyTableContainer = document.getElementById('historyTableContainer');
    const historyTable = document.createElement('table');

    // Generate the table content based on the history data
    // Similar to the logic used for generating the table in index.html

    historyTableContainer.appendChild(historyTable);
}
