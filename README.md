# Hostel Helpdesk AI

A demo that classifies hostel complaints into a fixed category and urgency, summarizes the issue, and suggests a safe next action.

## Features
- Classifies complaints into food, water, electricity, cleanliness, maintenance, security, internet, or other.
- Assigns low, medium, high, or critical urgency.
- Supports common Hinglish and messy inputs.
- Validates structured model output with Pydantic.
- Flags unclear and safety-related complaints for human review.
- Includes eight prompt test cases and automated structural tests.

## Run locally
1. Use Python 3.10+.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and add your own API key.
4. Run `streamlit run app.py`.
5. Run checks with `pip install pytest && python -m pytest -q`.

Never commit `.env` or expose your API key. Live model test outputs must be recorded after running the app; the repository does not claim the model tests have already been executed.

## Limitations
This is a demo, not an official college complaint channel. Staff must review critical or unclear cases. The app does not send complaints or create official tickets.
