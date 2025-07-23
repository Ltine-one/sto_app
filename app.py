
from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database.db'

def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    car TEXT,
                    service TEXT,
                    part TEXT,
                    date TEXT,
                    comment TEXT
                )
            """)

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    clients = conn.execute("SELECT * FROM clients ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", clients=clients)

@app.route('/add', methods=["POST"])
def add():
    data = (
        request.form['name'],
        request.form['phone'],
        request.form['car'],
        request.form['service'],
        request.form['part'],
        request.form['date'],
        request.form['comment']
    )
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        INSERT INTO clients (name, phone, car, service, part, date, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)
