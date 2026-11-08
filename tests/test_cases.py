import csv
from pathlib import Path
ROOT = Path(__file__).parents[1]
HEADERS = ["case_id", "type", "input", "expected_category", "expected_urgency", "expected_behaviour"]
def test_eight_cases_are_well_formed():
    with (ROOT / "prompt_cases.csv").open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert reader.fieldnames == HEADERS
    assert len(rows) == 8
    assert all(all((v or "").strip() for v in row.values()) for row in rows)
def test_expected_labels_are_allowed():
    with (ROOT / "prompt_cases.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    categories = {"food","water","electricity","cleanliness","maintenance","security","internet","other"}
    urgencies = {"low","medium","high","critical"}
    assert all(r["expected_category"] in categories for r in rows)
    assert all(r["expected_urgency"] in urgencies for r in rows)
def test_prompt_has_safety_rules():
    prompt = (ROOT / "prompts" / "complaint_sorter.txt").read_text(encoding="utf-8").lower()
    assert "do not invent" in prompt and "critical" in prompt
