import json
import os

LOG_FILE = "route_log.jsonl"

def log_route(intent, confidence, user_message, final_response):
    """
    Logs the routing decision and final response to a JSON Lines file.
    """
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
