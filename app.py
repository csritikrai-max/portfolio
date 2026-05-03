from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# 🔑 Get DB URL from Render
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# ✅ Create table
def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT,
        inquiry TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ✅ Home route
@app.route('/')
def home():
    return "Backend is running 🚀"

# ✅ Save form data
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data received"}), 400

        name = data.get('name')
        email = data.get('email')
        inquiry = data.get('inquiry')
        message = data.get('message')

        if not name or not email or not message:
            return jsonify({"message": "Missing required fields"}), 400

        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO contacts (name, email, inquiry, message)
        VALUES (%s, %s, %s, %s)
        """, (name, email, inquiry, message))

        conn.commit()
        conn.close()

        return jsonify({"message": "Message saved successfully!"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Server error"}), 500


# ✅ Get all data (JSON)
@app.route('/all', methods=['GET'])
def get_all():
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

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


# ✅ Dashboard (HTML table)
@app.route('/dashboard')
def dashboard():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body {
                font-family: Arial;
                background: #111;
                color: white;
                padding: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                border: 1px solid #444;
            }
            th {
                background: #00ff99;
                color: black;
            }
            tr:nth-child(even) {
                background: #1a1a1a;
            }
        </style>
    </head>
    <body>
        <h1>📊 Contact Form Data</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Inquiry</th>
                <th>Message</th>
            </tr>
    """

    for row in data:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


# ✅ Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)