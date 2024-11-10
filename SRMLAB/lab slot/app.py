from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for handling cross-origin requests
import pymysql

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

        # Insert booking data into the MySQL database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO lab_bookings (name, email, department, date, time_slot)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, department, date, time_slot))
            connection.commit()
        connection.close()

        # Return success message if the booking is successful
        return jsonify({'message': 'Slot booked successfully!'})

    except Exception as e:
        # Handle any errors that may occur and return error message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
