from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Create database and table
def init_db():
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            inquiry TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route to handle form submission
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    inquiry = data.get('inquiry')
    message = data.get('message')

    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (name, email, inquiry, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, inquiry, message))

    conn.commit()
    conn.close()

    return jsonify({"message": "Message saved successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)