# LLM-Powered Prompt Router for Intent Classification

This application intelligently routes user requests to specialized AI personas based on classified intent. It uses a two-step process: first, it classifies the user's intent using a lightweight LLM call, and then it routes the message to an expert persona for a high-quality, specialized response.

## Interface Options
- **Web UI (Recommended)**: A premium, modern dashboard to visualize classification and see expert responses.
- **Interactive CLI**: Real-time chat mode in the terminal.
- **Batch Testing**: Automated runner for the 20+ test scenarios.

## Project Structure
- `main.py`: Core logic for `classify_intent` (with manual override check) and `route_and_respond` (with confidence threshold).
- `prompts.json`: Configurable storage for system prompts and expert personas.
- `logger.py`: Utility for logging to JSON Lines format (`route_log.jsonl`).
- `test_router.py`: Batch test script covering 20+ scenarios including edge cases.
- `Dockerfile` & `docker-compose.yml`: Containerization setup.

## Setup Instructions
...
### Running with Docker
To build and run the application (which executes the test suite by default):
```bash
docker-compose up --build
```

**To run the Batch Tests:**
```bash
docker-compose run app python test_router.py
```

**To run the Interactive CLI:**
```bash
docker-compose run app python main.py
```

### Running Interactive CLI
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python main.py`

### Running Locally (Optional)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the test script:
   ```bash
   python test_router.py
   ```

## Design Decisions
- **Two-Step Routing**: Separating classification from response generation allows for more focused and accurate expert personas.
- **JSONL Logging**: Using JSON Lines for logging ensures that each entry is a complete JSON object, making it easy to parse and append to.
- **Fail-Safe Intent**: The system defaults to `unclear` for any parsing errors or low-confidence results, ensuring the user is always asked for clarification when the system is unsure.
