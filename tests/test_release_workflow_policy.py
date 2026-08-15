import re
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1] / ".github" / "workflows"


class ReleaseWorkflowPolicyTests(unittest.TestCase):
    def test_release_and_keepalive_workflows_are_manual_only(self) -> None:
        for filename in ("publish-dataset-release.yml", "keepalive.yml"):
            with self.subTest(workflow=filename):
                content = (WORKFLOW_DIR / filename).read_text(encoding="utf-8")
                on_block = content.split("\non:\n", maxsplit=1)[1].split("\n\n", maxsplit=1)[0]
                triggers = re.findall(r"^  ([A-Za-z_][A-Za-z0-9_-]*):", on_block, re.MULTILINE)

                self.assertIn("\n  workflow_dispatch:", content)
                self.assertEqual(triggers, ["workflow_dispatch"])
                self.assertNotIn("\n  schedule:", content)
                self.assertNotIn("cron:", content)

    def test_terminal_stewardship_and_rights_review_stay_owner_gated(self) -> None:
        repo_root = WORKFLOW_DIR.parents[1]
        rights = (repo_root / "RIGHTS.md").read_text(encoding="utf-8")
        roadmap = (repo_root / "ROADMAP.md").read_text(encoding="utf-8")
        readme = (repo_root / "README.md").read_text(encoding="utf-8")

        self.assertIn("no external contact is authorized", rights)
        self.assertIn("A no-red-flag or no-response outcome does not select a", rights)
        self.assertIn("browsertrix` maps to `high`", rights)
        self.assertIn("not a measured per-page quality score", rights)
        self.assertIn("443edd97278cf0c21bb525f24696dce2ddb61cad", rights)
        self.assertNotIn("inconsistent metadata requires governance review", rights)

        self.assertIn("Terminal event-triggered stewardship", roadmap)
        self.assertIn("no contact is authorized", roadmap)
        self.assertIn("prepared review packet is not authorization", roadmap)
        self.assertIn("No external review contact or outreach campaign is active", readme)


if __name__ == "__main__":
    unittest.main()
