from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            major TEXT NOT NULL,
            graduation_year INTEGER NOT NULL,
            internship_status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the ColorStack Member API"})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    conn = get_db()
    conn.execute(
        'INSERT INTO users (name, major, graduation_year, internship_status) VALUES (?, ?, ?, ?)',
        (data['name'], data['major'], data['graduation_year'], data['internship_status'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted successfully"}), 200

@app.route('/users/search', methods=['GET'])
def search_users():
    major = request.args.get('major')
    graduation_year = request.args.get('graduation_year')
    conn = get_db()
    query = 'SELECT * FROM users WHERE 1=1'
    params = []
    if major:
        query += ' AND major = ?'
        params.append(major)
    if graduation_year:
        query += ' AND graduation_year = ?'
        params.append(graduation_year)
    users = conn.execute(query, params).fetchall()
    conn.close()
    if not users:
        return jsonify({"error": "No users found"}), 404
    return jsonify([dict(u) for u in users])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)