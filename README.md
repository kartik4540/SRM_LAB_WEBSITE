SRM Lab Website
Project Overview
This project is a website for SRM Lab that provides essential information about the lab and allows users to book lab slots. The website is organized into different sections that cover contact details, lab specifications, schedules, and a booking slot feature for users to reserve lab time.

Project Structure
The website is organized into several directories, each containing specific files for the different sections of the website:

Folder and File Structure
graphql
Copy code
SRMLAB
├── contact
│   ├── contact.html         # Contact page with lab contact information
│   ├── script.js            # JavaScript for contact form functionality
│   ├── Srmseal.png          # SRM Lab logo or seal
│   └── styles.css           # Styles specific to the contact page
├── home
│   └── index.html           # Homepage with general information about SRM Lab
├── instructor
│   └── instructors.html     # Page with details about lab instructors
├── lab slot
│   ├── app.py               # Backend script for managing lab slot booking
│   ├── index.html           # Frontend for the slot booking page
│   ├── scripts.js           # JavaScript for handling slot booking logic
│   └── styleindex.css       # Styles specific to the slot booking page
├── schedule
│   └── schedule.html        # Page displaying the lab schedule
└── specification
    ├── specifications.html  # Page outlining lab specifications
    ├── script.js            # JavaScript for the specifications page
    ├── Srmseal.png          # Another copy of SRM Lab seal, if needed for styling
    └── styles.css           # Styles specific to the specifications page
Features
Homepage: Provides a general introduction to SRM Lab.
Contact Page: Contains contact information and a form for inquiries.
Instructors Page: Lists lab instructors along with their details.
Lab Slot Booking: Allows users to view available slots and book time in the lab.
Schedule Page: Displays the lab’s schedule and available slots.
Specifications Page: Contains detailed specifications of the lab equipment and resources.
Usage
Clone the repository to your local machine.
Navigate to the main directory and start the server (if applicable).
Open index.html in a web browser to explore the SRM Lab website.
To enable slot booking functionality, ensure that app.py is running as it provides the backend support for handling slot bookings.

Technologies Used
HTML, CSS, JavaScript for frontend design and interaction
Python (Flask/Django) for backend in app.py (assumed for handling bookings)
[Optional] Database for storing booking information (e.g., SQLite, MySQL)
