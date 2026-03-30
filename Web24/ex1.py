import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/error', methods=['GET'])
def error():
    app.logger.error("Simulated error at /error endpoint")
    return jsonify({"error": "Something went wrong"}), 500

@app.route('/user', methods=['POST'])
def user():
    data = request.get_json()
    
    if not data or "username" not in data:
        app.logger.warning("Attempt to access /user without username")
        return jsonify({"error": "Username is required"}), 400    

    username = data['username']
    app.logger.info(f"User greeted: {username}")
    return jsonify({"message": f"Hello, {username}!"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get("username") == "admin" and data.get("password") == "secret":
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)