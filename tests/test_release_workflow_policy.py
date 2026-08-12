import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1] / ".github" / "workflows"


class ReleaseWorkflowPolicyTests(unittest.TestCase):
    def test_release_and_keepalive_workflows_are_manual_only(self) -> None:
        for filename in ("publish-dataset-release.yml", "keepalive.yml"):
            with self.subTest(workflow=filename):
                content = (WORKFLOW_DIR / filename).read_text(encoding="utf-8")

                self.assertIn("\n  workflow_dispatch:", content)
                self.assertNotIn("\n  schedule:", content)
                self.assertNotIn("cron:", content)


if __name__ == "__main__":
    unittest.main()
