from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Frontend home route
@app.route("/")
def home():
    return jsonify({"message": "Frontend is running!"})

# Route that calls the Java backend
@app.route("/backend")
def backend():
    try:
        response = requests.get("http://localhost:8080")
        return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)