from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for handling cross-origin requests
import pymysql
from datetime import datetime, timedelta  # Import for date calculations

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='password',  # Replace with your MySQL password
        db='labbookingdb',    # Your updated database name
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to delete bookings older than one week
def delete_old_bookings():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Calculate the date one week ago
            one_week_ago = (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d')
            
            # SQL query to delete old bookings
            delete_sql = """
            DELETE FROM lab_bookings
            WHERE date < %s
            """
            cursor.execute(delete_sql, (one_week_ago,))
            connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error while deleting old bookings: {str(e)}")

# Function to validate email domain
def is_valid_srm_email(email):
    return email.endswith('@srmist.edu.in')

# Route to delete a specific booking
@app.route('/api/delete-slot', methods=['DELETE'])
def delete_slot():
    try:
        email = request.args.get('email')
        date = request.args.get('date')
        time_slot = request.args.get('timeSlot')

        # Validate required fields
        if not email or not date or not time_slot:
            return jsonify({'message': 'Email, date, and time slot are required to delete a booking.'}), 400

        connection = get_db_connection()
        with connection.cursor() as cursor:
            # First, check if a booking exists for the given email, date, and time slot
            check_sql = """
            SELECT * FROM lab_bookings
            WHERE email = %s AND date = %s AND time_slot = %s
            """
            cursor.execute(check_sql, (email, date, time_slot))
            booking = cursor.fetchone()

            if not booking:
                return jsonify({'message': 'No booking found for this email, date, and time slot.'}), 404

            # If a booking exists, delete it
            delete_sql = """
            DELETE FROM lab_bookings
            WHERE email = %s AND date = %s AND time_slot = %s
            """
            cursor.execute(delete_sql, (email, date, time_slot))
            connection.commit()

        connection.close()
        return jsonify({'message': 'Slot deleted successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle booking slot submissions
@app.route('/api/book-slot', methods=['POST'])
def book_slot():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        department = data.get('department')
        date = data.get('date')
        time_slot = data.get('timeSlot')

        # Validate registration length
        if not name or len(name) != 15:
            return jsonify({'message': 'Invalid registration number. It should be exactly 15 characters long.'}), 400

        # Validate email
        if not is_valid_srm_email(email.lower()):
            return jsonify({'message': 'Invalid email. Please use an email ending with @srmist.edu.in'}), 400

        # Validate the date to ensure it's not in the past
        current_date = datetime.now().date()
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        if selected_date < current_date:
            return jsonify({'message': 'Invalid date selected. Please select a date that is today or in the future.'}), 400

        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check if the user has already booked this slot
            check_duplicate_sql = """
            SELECT * FROM lab_bookings
            WHERE email = %s AND date = %s AND time_slot = %s
            """
            cursor.execute(check_duplicate_sql, (email, date, time_slot))
            existing_booking = cursor.fetchone()

            if existing_booking:
                return jsonify({'message': 'You have already booked this slot!'}), 400

            # Check the current number of bookings for the given date and time slot
            check_sql = """
            SELECT COUNT(*) as booking_count
            FROM lab_bookings
            WHERE date = %s AND time_slot = %s
            """
            cursor.execute(check_sql, (date, time_slot))
            result = cursor.fetchone()
            booking_count = result['booking_count']

            # If the slot is full, return an error message
            if booking_count >= 2:  # Slot is already full
                return jsonify({'message': 'This slot is already full! Please choose a different slot.'}), 400

            # Insert booking data into the database
            insert_sql = """
            INSERT INTO lab_bookings (name, email, department, date, time_slot)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (name.lower(), email.lower(), department, date, time_slot))
            connection.commit()

        connection.close()

        # Return success message if the booking is successful
        return jsonify({'message': 'Slot booked successfully!'})

    except Exception as e:
        # Handle any errors that may occur and return error message
        return jsonify({'error': str(e)}), 500

# Route to fetch available seats for each time slot on a given date
@app.route('/api/available-seats', methods=['GET'])
def get_available_seats():
    try:
        date = request.args.get('date')
        if not date:
            return jsonify({'error': 'Date is required'}), 400

        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Query to get the count of bookings for each time slot on the given date
            query = """
            SELECT time_slot, COUNT(*) as booking_count
            FROM lab_bookings
            WHERE date = %s
            GROUP BY time_slot
            """
            cursor.execute(query, (date,))
            results = cursor.fetchall()

            # Initialize a dictionary to hold the available seats for each time slot
            available_seats = {
                "9-11": 2,  # Maximum 2 seats per slot
                "11-1": 2,
                "2-4": 2,
                "4-6": 2
            }

            # Subtract the booked seats from the total available seats
            for result in results:
                time_slot = result['time_slot']
                booking_count = result['booking_count']
                available_seats[time_slot] -= booking_count

        connection.close()
        return jsonify(available_seats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to fetch booked slots for a user
@app.route('/api/booked-slots', methods=['GET'])
def get_booked_slots():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400

        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Query to get all booked slots for the given email
            query = """
            SELECT id, date, time_slot
            FROM lab_bookings
            WHERE email = %s
            """
            cursor.execute(query, (email,))
            results = cursor.fetchall()

        connection.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a specific booking by ID
@app.route('/api/delete-slot/<int:booking_id>', methods=['DELETE'])
def delete_slot_by_id(booking_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # SQL query to delete the booking by ID
            delete_sql = """
            DELETE FROM lab_bookings
            WHERE id = %s
            """
            cursor.execute(delete_sql, (booking_id,))
            connection.commit()

        connection.close()
        return jsonify({'message': 'Slot deleted successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Delete old bookings when the application starts
    delete_old_bookings()
    app.run(debug=True, port=8080)