from flask import Flask, request, jsonify
import heroku_applink as sdk  # AppLink SDK

app = Flask(__name__)
# AppLink middleware populates a secure client context on each request
app.wsgi_app = sdk.IntegrationWsgiMiddleware(app.wsgi_app, config=sdk.Config(request_timeout=5))

@app.route("/")
def health():
    return "Hello, Heroku! The app is running."

@app.route("/contact-count", methods=["POST"])
def contact_count():
    payload = request.get_json(silent=True) or {}
    account_id = payload.get("account_id")
    if not account_id:
        return jsonify({"error": "account_id is required"}), 400

    # Query Salesforce via AppLink's Data API using the invoking user's context
    data_api = sdk.get_client_context().data_api
    result = data_api.query(f"SELECT count() FROM Contact WHERE AccountId = '{account_id}'")

    # SDK returns an object with total_size; fall back if needed
    count = getattr(result, "total_size", None)
    if count is None and isinstance(result, dict):
        count = result.get("totalSize", 0)

    return jsonify({"account_id": account_id, "contact_count": int(count or 0)})

if __name__ == "__main__":
    app.run()
