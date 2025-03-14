document.addEventListener("DOMContentLoaded", function () {
    // Set the minimum date to today to prevent past dates from being selected
    let today = new Date().toISOString().split("T")[0];
    document.getElementById("date").setAttribute("min", today);

    // Fetch available seats when the date is selected
    document.getElementById("date").addEventListener("change", fetchAvailableSeats);

    // Add event listeners for form submission and slot deletion
    document.getElementById('labBookingForm').addEventListener('submit', handleFormSubmit);
    document.getElementById('fetchSlotsButton').addEventListener('click', fetchBookedSlots);
});

// Function to fetch available seats for the selected date
function fetchAvailableSeats() {
    const selectedDate = document.getElementById("date").value;

    if (!selectedDate) {
        alert("Please select a date to check available slots.");
        return;
    }

    // Show a loading indicator while fetching data
    const timeSlotSelect = document.getElementById("timeSlot");
    timeSlotSelect.innerHTML = "<option value=''>Loading available slots...</option>";

    fetch(`http://127.0.0.1:8080/api/available-seats?date=${selectedDate}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch available seats. Please try again.");
            }
            return response.json();
        })
        .then(data => updateTimeSlots(data))
        .catch(error => {
            console.error("Error fetching available seats:", error);
            alert(error.message);
            timeSlotSelect.innerHTML = "<option value=''>Error loading slots. Please try again.</option>";
        });
}

// Function to update the time slot dropdown with available seats
function updateTimeSlots(seatsData) {
    const timeSlotSelect = document.getElementById("timeSlot");
    timeSlotSelect.innerHTML = ""; // Clear existing options

    const timeSlots = [
        { value: "9-11", label: "9:00 AM - 11:00 AM" },
        { value: "11-1", label: "11:00 AM - 1:00 PM" },
        { value: "2-4", label: "2:00 PM - 4:00 PM" },
        { value: "4-6", label: "4:00 PM - 6:00 PM" }
    ];

    timeSlots.forEach(slot => {
        const availableSeats = seatsData[slot.value] || 0; // Get seats or default to 0
        const option = document.createElement("option");
        option.value = slot.value;
        option.textContent = `${slot.label} (${availableSeats} seats available)`;
        option.disabled = availableSeats === 0; // Disable if no seats left
        timeSlotSelect.appendChild(option);
    });

    // If no slots are available, show a message
    if (timeSlotSelect.options.length === 0) {
        timeSlotSelect.innerHTML = "<option value=''>No slots available for this date.</option>";
    }
}

// Function to handle form submission for booking a slot
function handleFormSubmit(event) {
    event.preventDefault();

    const booking = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        department: document.getElementById('department').value,
        date: document.getElementById('date').value,
        timeSlot: document.getElementById('timeSlot').value
    };

    // Validate form inputs
    if (!booking.name || !booking.email || !booking.date || !booking.timeSlot) {
        alert("Please fill out all fields before submitting.");
        return;
    }

    // Show a loading indicator while processing the booking
    const bookSlotButton = document.getElementById('bookSlotButton');
    bookSlotButton.textContent = "Booking...";
    bookSlotButton.disabled = true;

    fetch('http://127.0.0.1:8080/api/book-slot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(booking)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.message); });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchAvailableSeats(); // Refresh available seats after booking
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
    })
    .finally(() => {
        // Reset the button text and enable it
        bookSlotButton.textContent = "Book Slot";
        bookSlotButton.disabled = false;
    });
}

// Function to fetch booked slots for the user
function fetchBookedSlots() {
    const email = document.getElementById('deleteEmail').value.trim();

    if (!email) {
        alert("Please enter your email to fetch booked slots.");
        return;
    }

    // Show a loading indicator while fetching data
    const fetchSlotsButton = document.getElementById('fetchSlotsButton');
    fetchSlotsButton.textContent = "Fetching...";
    fetchSlotsButton.disabled = true;

    fetch(`http://127.0.0.1:8080/api/booked-slots?email=${encodeURIComponent(email)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error); });
            }
            return response.json();
        })
        .then(data => {
            const bookedSlotsList = document.getElementById('bookedSlotsList');
            bookedSlotsList.innerHTML = ""; // Clear existing list

            if (data.length === 0) {
                bookedSlotsList.innerHTML = "<li>No slots booked.</li>";
            } else {
                data.forEach(slot => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `Date: ${slot.date}, Time Slot: ${slot.time_slot}`;

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = "Delete";
                    deleteButton.addEventListener('click', () => deleteBookedSlot(slot.id, email));

                    listItem.appendChild(deleteButton);
                    bookedSlotsList.appendChild(listItem);
                });
            }

            // Show the booked slots container
            document.getElementById('bookedSlotsContainer').classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message);
        })
        .finally(() => {
            // Reset the button text and enable it
            fetchSlotsButton.textContent = "Fetch Booked Slots";
            fetchSlotsButton.disabled = false;
        });
}

// Function to delete a booked slot
function deleteBookedSlot(bookingId, email) {
    if (!confirm("Are you sure you want to delete this slot?")) {
        return;
    }

    fetch(`http://127.0.0.1:8080/api/delete-slot/${bookingId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchBookedSlots(); // Refresh the list after deletion
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
    });
}