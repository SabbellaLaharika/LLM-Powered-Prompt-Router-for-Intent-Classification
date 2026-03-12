import os
import json
import openai
from dotenv import load_dotenv
from logger import log_route

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load prompts
with open("prompts.json", "r") as f:
    PROMPTS = json.load(f)

def classify_intent(message: str) -> dict:
    """
    Calls an LLM to classify the user's intent.
    Returns: {"intent": str, "confidence": float}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
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
            "confidence": float(result["confidence"])
        }
    except Exception as e:
        print(f"Error in classify_intent: {e}")
        # Default to 'unclear' on any failure
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, intent_obj: dict) -> str:
    """
    Routes the user message to the correct expert based on intent.
    """
    intent = intent_obj["intent"]
    confidence = intent_obj["confidence"]
    
    # Check for 'unclear' or low confidence (low confidence is a stretch goal, but good practice)
    # The prompt explicitly says for 'unclear' intent, do not guess.
    if intent == "unclear" or intent not in PROMPTS["experts"]:
        final_response = PROMPTS["unclear_response"]
    else:
        # Get expert persona
        expert_prompt = PROMPTS["experts"][intent]
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",  # Using a more capable model for the expert responses
                messages=[
                    {"role": "system", "content": expert_prompt},
                    {"role": "user", "content": message}
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
    # Example usage
    test_message = "how do i sort a list of objects in python?"
    intent_obj = classify_intent(test_message)
    print(f"Detected Intent: {intent_obj}")
    response = route_and_respond(test_message, intent_obj)
    print(f"Response: {response}")
