from flask import Flask

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

if __name__ == '__main__':
    app.run(debug=True)
