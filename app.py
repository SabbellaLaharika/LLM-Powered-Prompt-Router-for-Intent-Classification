from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from main import classify_intent, route_and_respond
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/route", methods=["POST"])
def route_query():
    data = request.json
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
    
    # Use existing core logic
    intent_obj = classify_intent(message)
    response = route_and_respond(message, intent_obj)
    
    return jsonify({
        "intent": intent_obj["intent"],
        "confidence": intent_obj["confidence"],
        "manual_override": intent_obj.get("manual_override", False),
        "response": response
    })

if __name__ == "__main__":
    PORT = 5000
    try:
        app.run(host="0.0.0.0", port=PORT, debug=True)
    except OSError as e:
        if "address already in use" in str(e).lower() or "port is already allocated" in str(e).lower():
            print(f"\n[WARNING] Port {PORT} is already in use.")
            print(f"The Web UI could not start, but you can still use the CLI:")
            print(f"  > python main.py")
            print(f"\nTo use a different port, set the PORT environment variable or edit app.py.")
        else:
            raise e
