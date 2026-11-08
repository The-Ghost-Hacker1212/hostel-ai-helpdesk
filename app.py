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

def load_prompt() -> str:
    return (ROOT / "prompts" / "complaint_sorter.txt").read_text(encoding="utf-8")

def classify_complaint(message: str) -> ComplaintResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your local .env file.")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": load_prompt()},
            {"role": "user", "content": message}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "complaint_result",
                "strict": True,
                "schema": ComplaintResult.model_json_schema()
            }
        },
        temperature=0
    )
    raw = response.choices[0].message.content
    if not raw:
        raise RuntimeError("The model returned an empty response.")
    return ComplaintResult.model_validate_json(raw)

st.set_page_config(page_title="Hostel Helpdesk AI", page_icon="🏠", layout="centered")
st.title("🏠 Hostel Helpdesk AI")
st.caption("Turn a student's complaint into a validated category, urgency and next action.")

with st.expander("What this demo does"):
    st.write("The model classifies a complaint into a fixed category and urgency. The app validates the returned structure before displaying it.")
    st.write("Critical or uncertain complaints are flagged for human review. The model does not invent policies, deadlines, compensation or contact details.")

message = st.text_area(
    "Describe your hostel issue",
    placeholder="Example: Paani kal raat se nahi aa raha, bathroom use nahi kar paa rahe.",
    height=130
)

if st.button("Classify complaint", type="primary", use_container_width=True):
    if not message.strip():
        st.warning("Please enter a complaint first.")
    else:
        try:
            result = classify_complaint(message.strip())
            st.subheader("Validated result")
            col1, col2 = st.columns(2)
            col1.metric("Category", result.category.title())
            col2.metric("Urgency", result.urgency.title())
            st.write("**Summary**")
            st.write(result.summary)
            st.write("**Recommended action**")
            st.write(result.recommended_action)
            if result.needs_human_review:
                st.warning("Human review required.")
            else:
                st.success("No additional human review flag.")
            with st.expander("Structured JSON"):
                st.code(result.model_dump_json(indent=2), language="json")
        except Exception as exc:
            st.error(f"Could not produce a validated result: {exc}")
            st.info("Check your API key, model access and internet connection. Unvalidated answers are not displayed.")
