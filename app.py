from flask import Flask, request, jsonify

app = Flask(__name__)

# Root route (for browser testing)
@app.route("/", methods=["GET"])
def home():
    return "Flask server is running successfully!"

# Webhook route (for Dialogflow)
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    return jsonify({
        "fulfillmentText": "Webhook is working correctly!"
    })

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
