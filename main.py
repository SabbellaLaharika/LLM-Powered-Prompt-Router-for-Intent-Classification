import os
import json
import openai
from dotenv import load_dotenv
from logger import log_route

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or ""

# Configure client
if api_key.startswith("gsk_"):
    # Groq API Configuration
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    CLASSIFIER_MODEL = "llama-3.1-8b-instant"  # Latest fast model
    GENERATOR_MODEL = "llama-3.3-70b-versatile"   # Latest capable model
else:
    # Standard OpenAI Configuration
    client = openai.OpenAI(api_key=api_key)
    CLASSIFIER_MODEL = "gpt-3.5-turbo"
    GENERATOR_MODEL = "gpt-4"

# Load prompts
with open("prompts.json", "r") as f:
    PROMPTS = json.load(f)

CONFIDENCE_THRESHOLD = 0.7

def classify_intent(message: str) -> dict:
    """
    Calls an LLM to classify the user's intent.
    Returns: {"intent": str, "confidence": float}
    """
    # Check for manual override first
    for intent in PROMPTS["experts"].keys():
        if message.strip().lower().startswith(f"@{intent}"):
            # Strip the prefix and return manual intent with 1.0 confidence
            return {
                "intent": intent,
                "confidence": 1.0,
                "manual_override": True
            }

    try:
        response = client.chat.completions.create(
            model=CLASSIFIER_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies user intent into one of: code, data, writing, career, unclear."},
                {"role": "user", "content": PROMPTS["classification_prompt"].format(message=message)}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Validate schema
        if "intent" not in result or "confidence" not in result:
            raise ValueError("Invalid JSON schema from LLM")
            
        return {
            "intent": str(result["intent"]),
            "confidence": float(result["confidence"]),
            "manual_override": False
        }
    except Exception as e:
        print(f"Error in classify_intent: {e}")
        # Default to 'unclear' on any failure
        return {"intent": "unclear", "confidence": 0.0, "manual_override": False}

def route_and_respond(message: str, intent_obj: dict) -> str:
    """
    Routes the user message to the correct expert based on intent.
    """
    intent = intent_obj["intent"]
    confidence = intent_obj["confidence"]
    is_manual = intent_obj.get("manual_override", False)
    
    # Process message to remove suffix if manual
    clean_message = message
    if is_manual:
        clean_message = message.split(maxsplit=1)[1] if " " in message.strip() else ""

    # Check for 'unclear', low confidence, or invalid intent
    if (intent == "unclear" or 
        (not is_manual and confidence < CONFIDENCE_THRESHOLD) or 
        intent not in PROMPTS["experts"]):
        final_response = PROMPTS["unclear_response"]
    else:
        # Get expert persona
        expert_prompt = PROMPTS["experts"][intent]
        
        try:
            response = client.chat.completions.create(
                model=GENERATOR_MODEL,
                messages=[
                    {"role": "system", "content": expert_prompt},
                    {"role": "user", "content": clean_message}
                ],
                temperature=0.7
            )
            final_response = response.choices[0].message.content
        except Exception as e:
            print(f"Error in route_and_respond generation: {e}")
            final_response = "I encountered an error while processing your request. Could you try rephrasing?"

    # Log the decision
    log_route(intent, confidence, message, final_response)
    
    return final_response

if __name__ == "__main__":
    print("--- LLM-Powered Prompt Router Interactive Mode ---")
    print("Types of experts: code, data, writing, career")
    print("Use @expert_name prefix for manual override (e.g., @code Fix this)")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        intent_obj = classify_intent(user_input)
        print(f"[Intent: {intent_obj['intent']}, Confidence: {intent_obj['confidence']:.2f}, Manual: {intent_obj.get('manual_override', False)}]")
        
        response = route_and_respond(user_input, intent_obj)
        print(f"Assistant: {response}")
