document.getElementById('labBookingForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    const booking = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        department: document.getElementById('department').value,
        date: document.getElementById('date').value,
        timeSlot: document.getElementById('timeSlot').value
    };

    // Ensure the backend is running at the correct address (localhost:8080)
    fetch('http://127.0.0.1:8080/api/book-slot', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(booking)  // Send the booking details as JSON
    })
    .then(response => {
        if (response.ok) {
            return response.json();  // Parse the JSON response if status is OK
        } else {
            throw new Error('Failed to book slot');  // Handle non-OK responses
        }
    })
    .then(data => {
        // Show the success message returned by the backend
        alert(data.message);  // Or you could use something like: displaySuccessMessage(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while booking the slot. Please try again.');
    });
});
