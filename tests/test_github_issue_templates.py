import unittest
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / ".github" / "ISSUE_TEMPLATE"


class IssueTemplateContractTests(unittest.TestCase):
    def test_bug_report_contract(self) -> None:
        self._assert_template(
            "bug_report.md",
            "Bug report",
            [
                "## Affected release or artifact",
                "## What happened?",
                "## Reproduction and validation command",
                "## Expected integrity behavior",
                "## Environment",
                "## Additional context",
            ],
        )

    def test_feature_request_contract(self) -> None:
        self._assert_template(
            "feature_request.md",
            "Feature request",
            [
                "## Research or reproducibility need",
                "## Proposed metadata-only outcome",
                "## Release and compatibility implications",
                "## Alternatives considered",
                "## Validation",
            ],
        )

    def _assert_template(self, filename: str, expected_name: str, headings: list[str]) -> None:
        template = TEMPLATE_DIR / filename
        self.assertTrue(template.is_file(), f"missing issue template: {template}")

        content = template.read_text(encoding="utf-8")
        parts = content.split("---", maxsplit=2)
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0], "", "template must start with YAML frontmatter")

        frontmatter, body = parts[1], parts[2]
        self.assertIn(f"name: {expected_name}", frontmatter)
        self.assertIn("about:", frontmatter)
        self.assertIn('title: "', frontmatter)
        self.assertIn('labels: ""', frontmatter)
        self.assertIn('assignees: ""', frontmatter)

        for heading in headings:
            self.assertIn(heading, body)

        self.assertIn("SECURITY.md", body)
        self.assertIn("secret", body.lower())
        self.assertIn("private", body.lower())


if __name__ == "__main__":
    unittest.main()
