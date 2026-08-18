import tempfile
import unittest
from pathlib import Path

from source_reconstruction_status import build_status, reviewed_packets


class SourceReconstructionStatusTest(unittest.TestCase):
    def test_build_status_matches_review_summary_packets(self):
        source_findings = {
            "findings": [
                {
                    "priority": 1,
                    "smali_file": "smali_classes1/com/example/Reviewed.smali",
                    "class_name": "Lcom/example/Reviewed",
                    "jadx_file": "jadx/sources/com/example/Reviewed.java",
                    "category_counts": {"identifiers": 1},
                },
                {
                    "priority": 2,
                    "smali_file": "smali_classes1/com/example/Todo.smali",
                    "class_name": "Lcom/example/Todo",
                    "jadx_file": None,
                    "category_counts": {"location": 1},
                },
            ]
        }
        reviewed = {
            "smali_classes1/com/example/Reviewed.smali": "reviewed, static-only",
        }

        status = build_status(source_findings, reviewed)

        self.assertEqual(status["packet_count"], 2)
        self.assertEqual(status["reviewed_count"], 1)
        self.assertEqual(status["not_reviewed_count"], 1)
        self.assertEqual(status["jadx_count"], 1)
        self.assertEqual(status["rows"][0]["review_status"], "reviewed, static-only")
        self.assertEqual(status["rows"][1]["review_status"], "not reviewed")

    def test_reviewed_packets_parses_review_summary_table(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            notes = Path(tmpdir) / "reviewed_source_notes.md"
            notes.write_text(
                "\n".join(
                    [
                        "| Priority | Source packet | Reviewed status | Report value |",
                        "| --- | --- | --- | --- |",
                        "| 1 | `smali_classes1/com/example/Thing.smali` | reviewed, static-only | value |",
                    ]
                )
            )

            self.assertEqual(
                reviewed_packets(notes),
                {"smali_classes1/com/example/Thing.smali": "reviewed, static-only"},
            )


if __name__ == "__main__":
    unittest.main()
