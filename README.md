# Hostel Helpdesk AI

A small hackathon demo that classifies hostel complaints into a fixed category and urgency, then suggests a safe next action.

## Features
- Supports common English and Hinglish complaint text.
- Uses fixed category and urgency values.
- Requests schema-constrained JSON from the language model.
- Validates the model response with Pydantic before showing it.
- Flags unclear, unsafe and critical complaints for human review.
- Includes 8 test cases covering normal, edge and unsafe inputs.

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your own API key.
5. Start the app:

   ```bash
   streamlit run app.py
   ```

Do not commit `.env` or expose your API key in screenshots or a public repository.

## Test the case list

```bash
python -m pytest
```

Then paste each input from `prompt_cases.csv` into the app and save the actual JSON result. Compare the result with the expected behaviour; mark each run PASS or FAIL. Do not claim tests passed until you have run them.

## Repository structure

```text
hostel-ai-helpdesk/
├── app.py
├── prompts/
│   └── complaint_sorter.txt
├── prompt_cases.csv
├── tests/
│   └── test_cases.py
├── .env.example
├── .gitignore
├── requirements.txt
└── test_results_template.csv
```

## Limitations
- This is a demo, not an official college complaint channel.
- The model can make mistakes; staff must review critical or unclear cases.
- It does not send complaints, contact staff, or create official tickets.
- Configure the model and API key before the live demo.
