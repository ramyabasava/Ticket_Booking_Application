from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'tickets.db'

# Helper function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Close the database connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route 1: Main page
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT *, (total_seats - booked_seats) as available_seats FROM events")
    events = cursor.fetchall()
    return render_template('index.html', events=events)

# Route 2: Show booking form
@app.route('/event/<int:event_id>')
def event(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT *, (total_seats - booked_seats) as available_seats FROM events WHERE id = ?", (event_id,))
    event_details = cursor.fetchone()
    
    if event_details is None or event_details['available_seats'] <= 0:
        return redirect(url_for('index'))
        
    return render_template('booking.html', event=event_details)

# Route 3: Handle booking submission (UPDATED)
@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    event_id = request.form['event_id']
    num_tickets = int(request.form['num_tickets'])
    user_name = request.form['user_name']
    user_email = request.form['user_email']

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT booked_seats, total_seats, name FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()

    if event and (event['total_seats'] - event['booked_seats']) >= num_tickets:
        # 1. Update the booked seats count in the events table
        new_booked_seats = event['booked_seats'] + num_tickets
        cursor.execute("UPDATE events SET booked_seats = ? WHERE id = ?", (new_booked_seats, event_id))
        
        # 2. *** NEW: Insert the booking details into the bookings table ***
        cursor.execute("""
            INSERT INTO bookings (event_id, user_name, user_email, num_tickets)
            VALUES (?, ?, ?, ?)
        """, (event_id, user_name, user_email, num_tickets))

        db.commit() # Commit both the update and the insert together
        
        return redirect(url_for('confirmation', 
                                event_name=event['name'], 
                                num_tickets=num_tickets, 
                                user_name=user_name))
    else:
        return redirect(url_for('event', event_id=event_id))

# Route 4: Confirmation page (no changes needed)
@app.route('/confirmation')
def confirmation():
    event_name = request.args.get('event_name')
    num_tickets = request.args.get('num_tickets')
    user_name = request.args.get('user_name')
    return render_template('confirmation.html', event_name=event_name, num_tickets=num_tickets, user_name=user_name)

# --- NEW ROUTE TO VIEW BOOKINGS ---
@app.route('/bookings')
def view_bookings():
    db = get_db()
    cursor = db.cursor()
    # Use a JOIN to get the event name along with the booking details
    cursor.execute("""
        SELECT b.id, b.user_name, b.user_email, b.num_tickets, b.booking_date, e.name as event_name
        FROM bookings b
        JOIN events e ON b.event_id = e.id
        ORDER BY b.booking_date DESC
    """)
    bookings = cursor.fetchall()
    return render_template('bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)