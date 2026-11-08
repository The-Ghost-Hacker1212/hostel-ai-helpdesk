# Hostel Helpdesk AI

A free Streamlit prototype for hostel complaint triage.

## Modes
- **Free rules demo:** offline keyword-based classifier. No language model and no API key.
- **Local AI (Ollama):** real local language model, using the prompt in `prompts/complaint_sorter.txt`. No paid API credits. Requires installing Ollama and downloading a model. This mode has not yet been tested on the user's computer.

## Start
Install Python 3.10+, then:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Real local AI setup (free)
Install Ollama from https://ollama.com/download
Then run:
```bash
ollama pull llama3.2:3b
```
Make sure Ollama is running (on Windows it may run in the background). If necessary, start it with `ollama serve`. Select **Local AI (Ollama)** in the app. The model requires a download, disk space and enough RAM.

## Prompt engineering
The prompt specifies task, context, fixed output constraints, safety rules, and success conditions. The app validates JSON outputs and rejects unsupported labels or missing fields. See `prompt_cases.csv` for test inputs.

## Honest testing status
Screenshots from the earlier rules demo confirmed water, theft and smoke examples; an initial spoiled-food case failed and prompted a rule change. The Ollama mode is implemented but **has not been demonstrated to pass tests**. Do not claim model accuracy until you run and record outputs from the local model.

## Safety and privacy
This is not an emergency service. Classification can be wrong. All urgent complaints require human review. Do not upload personal data or API keys. `.env` is ignored by Git.
