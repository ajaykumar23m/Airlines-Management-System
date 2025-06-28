from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_no TEXT,
                    origin TEXT,
                    destination TEXT,
                    seats INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    flight_no TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    flights = conn.execute('SELECT * FROM flights').fetchall()
    conn.close()
    return render_template('index.html', flights=flights)

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        flight_no = request.form['flight_no']
        origin = request.form['origin']
        destination = request.form['destination']
        seats = request.form['seats']
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO flights (flight_no, origin, destination, seats) VALUES (?, ?, ?, ?)",
                (flight_no, origin, destination, seats))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_flight.html')

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    conn = sqlite3.connect('database.db')
    flights = conn.execute('SELECT flight_no, seats FROM flights WHERE seats > 0').fetchall()
    conn.close()
    if request.method == 'POST':
        name = request.form['name']
        flight_no = request.form['flight_no']
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO bookings (name, flight_no) VALUES (?, ?)", (name, flight_no))
        conn.execute("UPDATE flights SET seats = seats - 1 WHERE flight_no = ?", (flight_no,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('book_ticket.html', flights=flights)

@app.route('/view_bookings')
def view_bookings():
    conn = sqlite3.connect('database.db')
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('view_bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)
