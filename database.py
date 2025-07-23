import sqlite3

# Connect to the database
connection = sqlite3.connect('tickets.db')
cursor = connection.cursor()

# --- Drop existing tables to start fresh ---
cursor.execute("DROP TABLE IF EXISTS events")
cursor.execute("DROP TABLE IF EXISTS bookings") # Also drop the new table if it exists

# --- Create the events table ---
cursor.execute("""
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    total_seats INTEGER NOT NULL,
    booked_seats INTEGER NOT NULL DEFAULT 0,
    image_url TEXT
)
""")

# --- Create the NEW bookings table ---
# This table will store every booking made.
cursor.execute("""
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    user_email TEXT NOT NULL,
    num_tickets INTEGER NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events (id)
)
""")

# --- Add sample events (same as before) ---
sample_events = [
    ('Mumbai Music Festival', '2025-7-26', 'Starlight Area', 500, 120, 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc4fDB8MXxzZWFyY2h8Mnx8Y29uY2VydHxlbnwwfHx8fDE2NzExNjcxNTk&ixlib=rb-4.0.3&q=80&w=400'),
    ('Hackathon', '2025-8-15', 'Silicon Hall', 300, 250, 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc4fDB8MXxzZWFyY2h8NHx8Y29uZmVyZW5jZXxlbnwwfHx8fDE2NzExNjcyMTI&ixlib=rb-4.0.3&q=80&w=400'),
    ('Art & Soul Exhibition', '2025-8-01', 'The Grand Gallery', 150, 50, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc4fDB8MXxzZWFyY2h8M3x8YXJ0JTIwZ2FsbGVyeXxlbnwwfHx8fDE2NzExNjcyNDk&ixlib=rb-4.0.3&q=80&w=400'),
    ('Hyderabad Food Festival', '2025-9-20', 'Regal Cinema', 200, 195, '/static/images/food.png')
]


cursor.executemany("""
INSERT INTO events (name, date, location, total_seats, booked_seats, image_url)
VALUES (?, ?, ?, ?, ?, ?)
""", sample_events)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database 'tickets.db' with 'events' and 'bookings' tables created successfully!")