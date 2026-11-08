import os
from pathlib import Path
from typing import Literal

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
Category = Literal["food", "water", "electricity", "cleanliness", "maintenance", "security", "internet", "other"]
Urgency = Literal["low", "medium", "high", "critical"]

class ComplaintResult(BaseModel):
    category: Category
    urgency: Urgency
    summary: str = Field(min_length=5, max_length=180)
    recommended_action: str = Field(min_length=5, max_length=240)
    needs_human_review: bool

def classify_complaint(message: str) -> ComplaintResult:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Set OPENAI_API_KEY in your local .env file.")
    client = OpenAI(api_key=key)
    prompt = (ROOT / "prompts" / "complaint_sorter.txt").read_text(encoding="utf-8")
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role":"system","content":prompt},{"role":"user","content":message}],
        response_format={"type":"json_schema","json_schema":{"name":"complaint_result","strict":True,"schema":ComplaintResult.model_json_schema()}},
        temperature=0,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty response.")
    return ComplaintResult.model_validate_json(content)

st.set_page_config(page_title="Hostel Helpdesk AI", page_icon="🏠")
st.title("🏠 Hostel Helpdesk AI")
st.caption("Classify a hostel complaint and suggest a safe next action.")
message = st.text_area("Describe your hostel issue", placeholder="Paani kal raat se nahi aa raha...", height=130)
if st.button("Classify complaint", type="primary"):
    if not message.strip():
        st.warning("Please enter a complaint.")
    else:
        try:
            result = classify_complaint(message.strip())
            st.write("**Category:**", result.category)
            st.write("**Urgency:**", result.urgency)
            st.write("**Summary:**", result.summary)
            st.write("**Recommended action:**", result.recommended_action)
            if result.needs_human_review:
                st.warning("Human review required.")
            st.json(result.model_dump())
        except Exception as exc:
            st.error(f"Could not produce a validated result: {exc}")
