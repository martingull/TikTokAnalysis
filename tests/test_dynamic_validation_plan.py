import unittest

from dynamic_validation_plan import build_plan


SAMPLE_ANALYSIS = {
    "apk_path": "sample.apk",
    "app_name": "Sample",
    "package_name": "com.example.sample",
    "version_name": "1.0",
    "version_code": "100",
    "permissions": [
        "android.permission.CAMERA",
        "android.permission.RECORD_AUDIO",
    ],
    "exported_components": [
        "activity: com.example.DeepLinkActivity",
    ],
}


class DynamicValidationPlanTest(unittest.TestCase):
    def test_plan_includes_permission_and_source_driven_checks(self):
        source_findings = {
            "findings": [
                {
                    "smali_file": "smali_classes1/com/example/Thing.smali",
                    "category_counts": {
                        "identifiers": 2,
                        "network_telemetry": 1,
                    },
                }
            ]
        }

        plan = build_plan(SAMPLE_ANALYSIS, source_findings)

        self.assertIn("# Dynamic Privacy Validation Plan: Sample", plan)
        self.assertIn("Camera access", plan)
        self.assertIn("Microphone access", plan)
        self.assertIn("Device and advertising identifiers", plan)
        self.assertIn("Network telemetry", plan)
        self.assertIn("com.example.DeepLinkActivity", plan)


if __name__ == "__main__":
    unittest.main()
