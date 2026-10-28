"""Minimal test for lint.py over a temporary vault. Run: python scripts/test_lint.py"""
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint  # noqa: E402

FILES = {
    "wiki/index.md": "# Index\n- [[alpha]]\n",
    "wiki/concepts/alpha.md": "# Alpha\n[[beta]] [[missing]] [[areas/teses/_index|teses]]\n\n## Source(s)\n- x\n",
    "wiki/concepts/beta.md": "# Beta\nno sources here\n",
    "areas/teses/_index.md": "# Teses\n",
}


class LintTest(unittest.TestCase):
    def test_lint(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = Path(tmp)
            for rel, c in FILES.items():
                (v / rel).parent.mkdir(parents=True, exist_ok=True)
                (v / rel).write_text(c, encoding="utf-8")
            r = lint.lint(v)
        self.assertEqual(r["broken_links"], [("wiki/concepts/alpha.md", "missing")])
        self.assertEqual(r["orphans"], ["wiki/concepts/alpha.md"])
        self.assertEqual(r["index_gaps"], ["wiki/concepts/beta.md"])
        self.assertEqual(r["missing_sources"], ["wiki/concepts/beta.md"])


if __name__ == "__main__":
    unittest.main()
