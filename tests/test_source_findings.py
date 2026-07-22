import tempfile
import unittest
from pathlib import Path

from source_findings import build_findings, smali_class_to_java_path


class SourceFindingsTest(unittest.TestCase):
    def test_smali_class_maps_to_jadx_source_path(self):
        self.assertEqual(
            smali_class_to_java_path("Lcom/example/Thing", "jadx_out"),
            Path("jadx_out/sources/com/example/Thing.java"),
        )

    def test_build_findings_pairs_smali_and_jadx_context(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            decompile_dir = root / "apktool"
            smali_path = decompile_dir / "smali_classes1/com/example/Thing.smali"
            smali_path.parent.mkdir(parents=True)
            smali_path.write_text(
                "\n".join(
                    [
                        ".class public Lcom/example/Thing;",
                        ".method public test()V",
                        "invoke-virtual {v0}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;",
                        ".end method",
                    ]
                )
            )

            jadx_dir = root / "jadx"
            java_path = jadx_dir / "sources/com/example/Thing.java"
            java_path.parent.mkdir(parents=True)
            java_path.write_text("class Thing { void test() { Runtime.getRuntime().exec(\"id\"); } }\n")

            inventory = {
                "selected_source_slices": [
                    {
                        "file": "smali_classes1/com/example/Thing.smali",
                        "class_name": "Lcom/example/Thing",
                        "weighted_score": 7,
                        "total_matches": 1,
                        "category_counts": {"command_execution": 1},
                        "findings": [
                            {
                                "line": 3,
                                "category": "command_execution",
                                "keyword": "Runtime",
                                "method": ".method public test()V",
                                "code": "invoke-virtual",
                            }
                        ],
                    }
                ]
            }

            payload = build_findings(inventory, decompile_dir, jadx_dir, 10, 1, 5)
            finding = payload["findings"][0]

            self.assertEqual(finding["jadx_file"], str(java_path))
            self.assertEqual(finding["smali_context"][0]["line"], 3)
            self.assertEqual(finding["jadx_matches"][0]["line"], 1)


if __name__ == "__main__":
    unittest.main()
