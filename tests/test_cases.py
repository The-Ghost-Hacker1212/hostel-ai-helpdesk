import csv
from pathlib import Path

def test_case_file_has_at_least_eight_cases():
    path = Path(__file__).parents[1] / "prompt_cases.csv"
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 8
    assert all(row["type"] in {"normal", "edge", "unsafe"} for row in rows)
    assert all(row["expected_behaviour"].strip() for row in rows)
