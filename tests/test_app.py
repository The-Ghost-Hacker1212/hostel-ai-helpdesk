import unittest
from pathlib import Path

# Run tests without importing Streamlit UI; extract pure functions.
# Simple integration checks use subprocess in CI if Streamlit is installed.
class ProjectFilesTest(unittest.TestCase):
    def test_prompt_exists(self):
        self.assertTrue(Path("prompts/complaint_sorter.txt").is_file())

    def test_cases_exist(self):
        self.assertGreaterEqual(len(Path("prompt_cases.csv").read_text().splitlines()), 9)

    def test_no_api_key_needed(self):
        self.assertNotIn("OPENAI_API_KEY", Path("app.py").read_text())

if __name__ == "__main__":
    unittest.main()
