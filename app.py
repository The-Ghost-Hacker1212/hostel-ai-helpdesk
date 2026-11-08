import json
import re
import urllib.request
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent
CATEGORIES = ["food", "water", "electricity", "cleanliness", "maintenance", "security", "internet", "other"]
URGENCIES = ["low", "medium", "high", "critical"]
KEYWORDS = {
    "security": ["stole", "stolen", "theft", "robbed", "harass", "threat", "chori", "intruder"],
    "water": ["water", "paani", "pani", "tap"],
    "food": ["food", "mess", "meal", "spoiled", "rotten", "khana"],
    "electricity": ["electric", "power", "bijli", "sparking"],
    "cleanliness": ["dirty", "garbage", "toilet", "bathroom", "cockroach", "rats"],
    "maintenance": ["broken", "repair", "leak", "door", "window", "ceiling"],
    "internet": ["internet", "wifi", "wi-fi", "router", "network"],
}
ACTIONS = {
    "security": "Contact hostel security and the warden; preserve evidence and avoid confronting suspects.",
    "water": "Report the water outage to the warden and maintenance team.",
    "food": "Report to the mess supervisor and warden; avoid suspected spoiled food and seek medical help for severe symptoms.",
    "electricity": "Notify maintenance; stay away from damaged electrical equipment.",
    "cleanliness": "Report the affected area to housekeeping.",
    "maintenance": "Request maintenance and avoid using damaged equipment.",
    "internet": "Report the problem to hostel IT support.",
    "other": "Ask the hostel office or warden to review this complaint.",
}
def classify_rules(message):
    t = re.sub(r"\s+", " ", message.lower())
    scores = {k: sum(w in t for w in words) for k, words in KEYWORDS.items()}
    category = max(scores, key=scores.get)
    if not scores[category]:
        category = "other"
    critical = any(w in t for w in ["fire", "smoke", "gas leak", "electric shock", "unconscious", "weapon"])
    high = any(w in t for w in ["stole", "stolen", "theft", "robbed", "harass", "threat", "chori", "no water", "spoiled", "food poisoning", "several students", "vomiting", "flood"])
    medium = any(w in t for w in ["since last night", "since yesterday", "not working", "for hours"])
    urgency = "critical" if critical else "high" if high else "medium" if medium else "low"
    if category == "food" and any(w in t for w in ["spoiled", "sick", "rotten", "vomit"]):
        urgency = "high"
    action = ACTIONS[category]
    if urgency == "critical":
        action = "Move away from danger if safe; contact hostel security and emergency services. Do not handle the hazard yourself."
    return {"category": category, "urgency": urgency, "summary": message.strip()[:180],
            "recommended_action": action,
            "needs_human_review": urgency in ("high", "critical") or category in ("security", "other")}

def validate(value):
    if not isinstance(value, dict):
        raise ValueError("Response is not an object")
    for key in ("category", "urgency", "summary", "recommended_action", "needs_human_review"):
        if key not in value:
            raise ValueError("Missing field: " + key)
    if value["category"] not in CATEGORIES or value["urgency"] not in URGENCIES:
        raise ValueError("Unsupported label")
    if not isinstance(value["needs_human_review"], bool):
        raise ValueError("Human review must be boolean")
    for key, maximum in (("summary", 180), ("recommended_action", 300)):
        if not isinstance(value[key], str) or not 5 <= len(value[key]) <= maximum:
            raise ValueError("Invalid " + key)
    if value["urgency"] in ("high", "critical") or value["category"] == "security":
        value["needs_human_review"] = True
    return value

def classify_local_ai(message, model):
    prompt = (ROOT / "prompts" / "complaint_sorter.txt").read_text(encoding="utf-8")
    body = json.dumps({"model": model, "stream": False, "format": "json",
        "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": message}]}).encode("utf-8")
    request = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=body,
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)
    return validate(json.loads(result["message"]["content"]))

st.set_page_config(page_title="Hostel Helpdesk AI", page_icon="🏠")
st.title("🏠 Hostel Helpdesk AI")
st.caption("Classify hostel complaints and suggest safe next actions.")
mode = st.radio("Choose mode", ["Free rules demo", "Local AI (Ollama)"], horizontal=True)
if mode == "Free rules demo":
    st.info("Free offline rules demo. This mode is not a language model.")
else:
    st.info("Uses a real local language model via Ollama; no paid API credits.")
model = st.text_input("Local model name", "llama3.2:3b") if mode == "Local AI (Ollama)" else ""
message = st.text_area("Describe your hostel issue", height=130)
if st.button("Classify complaint", type="primary"):
    if not message.strip():
        st.warning("Enter a complaint.")
    else:
        try:
            result = classify_rules(message) if mode == "Free rules demo" else classify_local_ai(message, model)
            st.subheader("Complaint result")
            for key, value in result.items():
                st.write("**" + key.replace("_", " ").title() + ":**", value)
            st.json(result)
        except Exception as exc:
            st.error("Could not produce a validated result. For local AI, check Ollama and model installation: " + str(exc))
st.caption("Prototype only. Human review is essential; never rely on this for emergencies.")
