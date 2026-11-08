import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
EXPECTED_HEADERS = [
    "case_id", "type", "input", "expected_category",
    "expected_urgency", "expected_behaviour"
]

def load_cases():
    with (ROOT / "prompt_cases.csv").open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == EXPECTED_HEADERS
        return list(reader)

def test_case_file_has_eight_well_formed_cases():
    rows = load_cases()
    assert len(rows) == 8
    assert all(row["type"] in {"normal", "edge", "unsafe"} for row in rows)
    assert all(all((value or "").strip() for value in row.values()) for row in rows)

def test_expected_labels_use_allowed_values():
    rows = load_cases()
    categories = {"food", "water", "electricity", "cleanliness", "maintenance", "security", "internet", "other"}
    urgencies = {"low", "medium", "high", "critical"}
    assert all(row["expected_category"] in categories for row in rows)
    assert all(row["expected_urgency"] in urgencies for row in rows)

def test_prompt_contains_safety_and_no_invention_rules():
    prompt = (ROOT / "prompts" / "complaint_sorter.txt").read_text(encoding="utf-8").lower()
    assert "do not invent" in prompt
    assert "critical" in prompt
    assert "human review" in prompt
