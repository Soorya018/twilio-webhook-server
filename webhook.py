from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse
import json
import os
from typing import Dict, Any

app = Flask(__name__)

RESULTS_FILE = "results.json"

# Ensure the results file exists
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "w") as f:
        json.dump({}, f)

def load_results() -> Dict[str, Any]:
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)

def save_results(data: Dict[str, Any]) -> None:
    with open(RESULTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Route that Twilio uses to control the voice call
@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say("Hello. This is your autodialer call. Have a good day.")
    return str(response)

# Route that Twilio uses to report call status
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.form

    call_sid = data.get("CallSid")
    call_status = data.get("CallStatus")
    to_number = data.get("To")
    from_number = data.get("From")

    if not call_sid and not to_number:
        return jsonify({"error": "Missing CallSid or To number"}), 400

    key = call_sid or to_number
    results = load_results()

    results.setdefault(key, []).append({
        "status": call_status,
        "to": to_number,
        "from": from_number
    })

    save_results(results)
    return jsonify({"status": "received", "call_status": call_status}), 200

# Route to view saved results (for debugging)
@app.route("/results", methods=["GET"])
def get_results():
    return jsonify(load_results())

if __name__ == "__main__":
    app.run(debug=True)
