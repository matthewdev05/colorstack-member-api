from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Matthew", "major": "Computer Science"},
    {"id": 2, "name": "Jessica", "major": "Physics"},
    {"id": 3, "name": "David", "major": "Math"}
]

@app.route('/')
def home():
    return {"message": "Welcome to my API!"}

@app.route('/users')
def get_users():
    return {"users": users}

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_id = max(u["id"] for u in users) + 1

    new_user = {
        "id": new_id,
        "name": data["name"],
        "major": data["major"]
    }

    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)