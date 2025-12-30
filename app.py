from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# =========================
# MEMORY SETUP
# =========================
MEMORY_FILE = "progress.json"

# Create memory file if it does not exist
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({
            "topics_completed": [],
            "weak_topics": [],
            "quiz_scores": {}
        }, f, indent=4)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# ROOT ROUTE (Browser Test)
# =========================
@app.route("/", methods=["GET"])
def home():
    return "Flask server is running successfully!"

# =========================
# WEBHOOK ROUTE (Dialogflow)
# =========================
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.get_json(silent=True)

    # If opened in browser
    if req is None:
        return jsonify({
            "fulfillmentText": "Webhook is working correctly!"
        })

    intent = req["queryResult"]["intent"]["displayName"]
    parameters = req["queryResult"]["parameters"]

    memory = load_memory()

    # STUDY PLAN INTENT
    if intent == "Study.plan":
        days = parameters.get("exam_days", "few")
        subject = parameters.get("subject", "your subject")

        response_text = f"I will create a {days}-day smart study plan for {subject}."

        return jsonify({"fulfillmentText": response_text})

    # QUIZ EVALUATION INTENT (Example)
    if intent == "quiz.evaluate":
        topic = parameters.get("topic", "Unknown Topic")
        score = parameters.get("score", 40)

        memory["quiz_scores"][topic] = score

        if score < 50:
            if topic not in memory["weak_topics"]:
                memory["weak_topics"].append(topic)
            save_memory(memory)
            return jsonify({
                "fulfillmentText": f"You are weak in {topic}. I suggest revising it tomorrow."
            })
        else:
            save_memory(memory)
            return jsonify({
                "fulfillmentText": f"Good job in {topic}! You can move to the next topic."
            })

    return jsonify({
        "fulfillmentText": "Request received successfully."
    })

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
