import tempfile
import unittest
from pathlib import Path

from security_markers import scan_security_markers


class SecurityMarkersTest(unittest.TestCase):
    def test_scan_security_markers_counts_categories_and_exports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            decompile_dir = Path(tmpdir) / "apktool"
            smali_path = decompile_dir / "smali_classes1/com/example/Shell.smali"
            smali_path.parent.mkdir(parents=True)
            smali_path.write_text(
                "\n".join(
                    [
                        ".class public Lcom/example/Shell;",
                        ".method public run()V",
                        "invoke-virtual {v0, v1}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;",
                        "new-instance v2, Ldalvik/system/DexClassLoader;",
                        "invoke-virtual {v3, v4}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V",
                        ".end method",
                    ]
                )
            )

            analysis = {
                "apk_path": "sample.apk",
                "package_name": "com.example",
                "version_name": "1.0",
                "exported_components": ["activity: com.example.DeepLinkActivity"],
            }

            payload = scan_security_markers(analysis, decompile_dir, limit=10, max_findings=5)

            self.assertEqual(payload["exported_component_count"], 1)
            self.assertEqual(payload["categories"]["command_execution"]["total_matches"], 1)
            self.assertEqual(payload["categories"]["dynamic_code_loading"]["total_matches"], 1)
            self.assertEqual(payload["categories"]["webview_bridge"]["total_matches"], 1)
            self.assertEqual(payload["selected_files"][0]["class_name"], "Lcom/example/Shell")
            self.assertEqual(payload["selected_files"][0]["triage"]["triggerability"], "unknown")

    def test_scan_security_markers_avoids_broad_substring_false_positives(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            decompile_dir = Path(tmpdir) / "apktool"
            smali_path = decompile_dir / "smali_classes1/com/example/Noise.smali"
            smali_path.parent.mkdir(parents=True)
            smali_path.write_text(
                "\n".join(
                    [
                        ".class public Lcom/example/Noise;",
                        ".method public probe()V",
                        "invoke-static {}, Landroid/os/Environment;->getDataDirectory()Ljava/io/File;",
                        "invoke-virtual {v0}, Landroid/app/usage/StorageStats;->getDataBytes()J",
                        "instance-of v0, v1, Ldalvik/system/BaseDexClassLoader;",
                        ".end method",
                    ]
                )
            )

            payload = scan_security_markers({}, decompile_dir, limit=10, max_findings=5)

            self.assertEqual(payload["categories"]["intent_entrypoints"]["total_matches"], 0)
            self.assertEqual(payload["categories"]["dynamic_code_loading"]["total_matches"], 1)
            self.assertEqual(payload["keyword_totals"], {"BaseDexClassLoader": 1})


if __name__ == "__main__":
    unittest.main()
