from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# ✅ Database path (safe for Render)
DB_PATH = os.path.join(os.getcwd(), 'contact.db')

# ✅ Create database and table
def init_db():
    conn = sqlite3.connect(DB_PATH)
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

# ✅ Home route (to check server is running)
@app.route('/')
def home():
    return "Backend is running 🚀"

# ✅ Save form data
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        print("Received data:", data)  # 🔥 debug log

        if not data:
            return jsonify({"message": "No data received"}), 400

        name = data.get('name')
        email = data.get('email')
        inquiry = data.get('inquiry')
        message = data.get('message')

        if not name or not email or not message:
            return jsonify({"message": "Missing required fields"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, inquiry, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, inquiry, message))

        conn.commit()
        conn.close()

        return jsonify({"message": "Message saved successfully!"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Server error"}), 500

# ✅ NEW: View all stored data in browser
@app.route('/all', methods=['GET'])
def get_all():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        conn.close()

        # Convert to readable JSON
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "inquiry": row[3],
                "message": row[4]
            })

        return jsonify(data)

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error fetching data"}), 500


# ✅ Run app (for local)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)