from main import classify_intent, route_and_respond

test_messages = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "this paragraph sounds awkward, can you help me fix it?",
    "i'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds? (Should be 'unclear')",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose."
]

def run_tests():
    print(f"{'#'*20} Starting Routing Tests {'#'*20}")
    for i, msg in enumerate(test_messages, 1):
        print(f"\nTest {i}: {msg}")
        intent_obj = classify_intent(msg)
        print(f"Detected Intent: {intent_obj['intent']} (Confidence: {intent_obj['confidence']:.2f})")
        response = route_and_respond(msg, intent_obj)
        print(f"Final Response: {response[:150]}...") # Print first 150 chars
    print(f"\n{'#'*20} Tests Completed {'#'*20}")

if __name__ == "__main__":
    run_tests()
