// JavaScript to handle dynamic alert box based on threat detection
let alertBox = document.getElementById('alert-box');
let alertMessage = document.getElementById('alert-message');

// Function to check if a threat is detected from the backend
function checkThreat() {
    fetch('/check_threat')
        .then(response => response.json())
        .then(data => {
            if (data.threat_detected) {
                alertMessage.textContent = "Threat Detected!";
                alertBox.style.display = "block"; // Show the alert box
            } else {
                alertMessage.textContent = "No Threat Detected";
                alertBox.style.display = "none";  // Hide the alert box
            }
        })
        .catch(error => console.error('Error checking threat:', error));
}

// Function to update time
function updateTime() {
    const now = new Date();
    document.getElementById('live-time').textContent = now.toLocaleTimeString();
}

// Update time every second
setInterval(updateTime, 1000);

// Function to fetch location (placeholder)
function fetchLocation() {
    document.getElementById('live-location').textContent = "Pune, India"; // Placeholder, integrate with GPS API if needed
}

// Check for threat status every 1 second
setInterval(checkThreat, 1000);

// Fetch initial location
fetchLocation();
