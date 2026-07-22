import unittest

from dashboard import normalize_report
from report_builder import build_report


SAMPLE_ANALYSIS = {
    "analysis_schema_version": 1,
    "apk_path": "sample.apk",
    "app_name": "Sample",
    "package_name": "com.example.sample",
    "version_name": "1.0",
    "version_code": "100",
    "permissions": [
        "android.permission.CAMERA",
        "android.permission.RECORD_AUDIO",
    ],
    "component_counts": {
        "permissions": 2,
        "activities": 1,
        "services": 0,
        "broadcast_receivers": 0,
        "content_providers": 0,
    },
    "certificate_info": {
        "is_signed": True,
        "is_signed_v1": True,
        "is_signed_v2": False,
        "is_signed_v3": False,
        "certificates": [
            {
                "subject": "CN=sample",
                "issuer": "CN=sample",
                "not_valid_before": "2020-01-01T00:00:00",
                "not_valid_after": "2040-01-01T00:00:00",
                "sha1": "abc",
                "sha256": "def",
            }
        ],
    },
    "metadata": {
        "Main Activity": "com.example.MainActivity",
        "Target SDK": "35",
        "Min SDK": "23",
    },
    "suspicious_behavior": {
        "Privacy Invasion": ["Landroid/hardware/Camera;->open"],
    },
    "permission_api_map": {
        "android.permission.CAMERA": {
            "declared": True,
            "references": ["Landroid/hardware/Camera;->open"],
        },
        "android.permission.ACCESS_FINE_LOCATION": {
            "declared": False,
            "references": ["Landroid/location/LocationManager;->getLastKnownLocation"],
        },
    },
    "exported_components": ["activity: com.example.MainActivity"],
}


class Path1SchemaTest(unittest.TestCase):
    def test_dashboard_normalizes_rich_certificate_schema(self):
        normalized = normalize_report(SAMPLE_ANALYSIS)

        self.assertEqual(normalized["certificate"]["Subject"], "CN=sample")
        self.assertEqual(normalized["certificate"]["SHA256"], "def")
        self.assertEqual(
            normalized["permission_api_map"]["android.permission.ACCESS_FINE_LOCATION"]["declared"],
            False,
        )

    def test_report_builder_surfaces_certificate_and_declared_mapping(self):
        report = build_report(SAMPLE_ANALYSIS)

        self.assertIn("### Certificate And Signing", report)
        self.assertIn("| Subject | CN=sample |", report)
        self.assertIn("| android.permission.CAMERA | True |", report)
        self.assertIn("| android.permission.ACCESS_FINE_LOCATION | False |", report)

    def test_report_builder_includes_source_finding_packets_when_supplied(self):
        source_findings = {
            "findings": [
                {
                    "priority": 1,
                    "smali_file": "smali_classes1/com/example/Thing.smali",
                    "class_name": "Lcom/example/Thing",
                    "jadx_file": "jadx_decompiled/sources/com/example/Thing.java",
                    "category_counts": {"command_execution": 1},
                    "smali_context": [
                        {
                            "line": 12,
                            "category": "command_execution",
                            "keyword": "Runtime",
                            "context": [
                                {
                                    "line": 12,
                                    "code": "invoke-virtual {v0}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;",
                                }
                            ],
                        }
                    ],
                    "jadx_matches": [
                        {
                            "line": 7,
                            "code": 'Runtime.getRuntime().exec("id");',
                        }
                    ],
                }
            ]
        }

        report = build_report(SAMPLE_ANALYSIS, source_findings=source_findings)

        self.assertIn("## Source Finding Packets", report)
        self.assertIn("smali_classes1/com/example/Thing.smali", report)
        self.assertIn("Line 12", report)
        self.assertIn("Runtime.getRuntime().exec", report)

    def test_report_builder_includes_reviewed_source_notes_when_supplied(self):
        report = build_report(SAMPLE_ANALYSIS, reviewed_notes="Reviewed behavior: API hook dictionary.")

        self.assertIn("## Reviewed Source Notes", report)
        self.assertIn("Reviewed behavior: API hook dictionary.", report)


if __name__ == "__main__":
    unittest.main()
