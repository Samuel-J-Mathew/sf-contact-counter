from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def health():
    return "Hello, Heroku! The app is running."

@app.route("/contact-count", methods=["POST"])
def contact_count():
    data = request.get_json(silent=True) or {}
    account_id = data.get("account_id")
    return jsonify({"account_id": account_id, "contact_count": 5})

if __name__ == "__main__":
    app.run()
