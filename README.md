# Hostel Helpdesk AI

A Streamlit demo that classifies hostel complaints into a fixed category and urgency, summarizes the issue, and suggests a safe next action.

## Features
- Fixed complaint categories and urgency levels.
- Handles common Hinglish and unclear messages.
- Validates structured model output with Pydantic.
- Flags critical and unclear cases for human review.
- Includes eight prompt test cases and automated structural tests.

## Run locally
1. Install Python 3.10+.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and add your own `OPENAI_API_KEY`.
4. Run `streamlit run app.py`.
5. Run checks: `pip install pytest && python -m pytest -q`.

Never commit `.env` or expose your API key. Live model test outputs must be recorded after running the app; do not claim they passed until actually run.

## Limitations
This is a demo, not an official complaint channel. Staff must review critical or unclear cases. The app does not send complaints or create official tickets.
