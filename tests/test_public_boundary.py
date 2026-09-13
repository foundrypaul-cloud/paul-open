import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SANITIZER_SPEC = importlib.util.spec_from_file_location(
    "sanitize_kaggle_public_evidence",
    ROOT / "scripts" / "sanitize_kaggle_public_evidence.py",
)
SANITIZER = importlib.util.module_from_spec(SANITIZER_SPEC)
assert SANITIZER_SPEC and SANITIZER_SPEC.loader
SANITIZER_SPEC.loader.exec_module(SANITIZER)

GUARD_SPEC = importlib.util.spec_from_file_location(
    "check_public_boundary",
    ROOT / "scripts" / "check_public_boundary.py",
)
GUARD = importlib.util.module_from_spec(GUARD_SPEC)
assert GUARD_SPEC and GUARD_SPEC.loader
GUARD_SPEC.loader.exec_module(GUARD)


class PublicBoundarySanitizerTest(unittest.TestCase):
    def test_raw_case_data_seed_paths_and_secrets_are_not_copied(self):
        with tempfile.TemporaryDirectory() as tmp:
            private = Path(tmp) / "private"
            private.mkdir()
            fake_token = "KGAT_" + "never_public_fixture_token_value"
            (private / "sft_results.json").write_text(
                json.dumps(
                    {
                        "manifest": {
                            "experiment_id": "exp_test",
                            "completed_cases": 1,
                            "failed_cases": 0,
                            "total_cases": 1,
                            "status": "SUCCESS",
                            "local_results_path": "/private/result.json",
                        },
                        "metadata": {
                            "random_seed": 987654,
                            "sampling_parameters": {"temperature": 0.2},
                        },
                        "overall_summary": {
                            "total_cases_evaluated": 1,
                            "mean_rubric_score": 91.0,
                        },
                        "case_results": [
                            {
                                "case_id": "sealed-1",
                                "prompt": "NEVER_PUBLIC_PROMPT",
                                "response": "NEVER_PUBLIC_RESPONSE",
                                "token": fake_token,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (private / "failure_summary.json").write_text(
                json.dumps(
                    {
                        "status": "FAILED",
                        "failed_stage": "generation",
                        "exception_type": "RuntimeError",
                        "sanitized_message": "private path /kaggle/input/internal-source",
                    }
                ),
                encoding="utf-8",
            )

            public = SANITIZER.collect(private)
            text = json.dumps(public, sort_keys=True)

            self.assertIn("mean_rubric_score", text)
            self.assertIn("failed_stage", text)
            for forbidden in (
                "case_results",
                "NEVER_PUBLIC_PROMPT",
                "NEVER_PUBLIC_RESPONSE",
                "random_seed",
                "sampling_parameters",
                "local_results_path",
                "sanitized_message",
                fake_token,
                "/kaggle/input/internal-source",
            ):
                self.assertNotIn(forbidden, text)

    def test_h6_stage_is_normalized_without_copying_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            private = Path(tmp) / "private"
            private.mkdir()
            path = private / "failure_summary.json"
            path.write_text(
                json.dumps(
                    {
                        "status": "FAILED",
                        "stage": "dhe_generation",
                        "exception_type": "RuntimeError",
                        "message": "sensitive private detail",
                    }
                ),
                encoding="utf-8",
            )
            public = SANITIZER.sanitize_json(path, "failure")
            self.assertEqual(public["failed_stage"], "dhe_generation")
            self.assertNotIn("stage", public)
            self.assertNotIn("message", public)


class PublicBoundaryGuardTest(unittest.TestCase):
    def test_extensionless_utf8_file_is_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "id_rsa"
            marker = "-----BEGIN " + "PRIVATE KEY-----"
            path.write_text(marker + "\nfixture\n", encoding="utf-8")
            text = GUARD.read_text(path)
            self.assertIsNotNone(text)
            self.assertRegex(text, GUARD.SECRET_PATTERNS["PEM private key"])

    def test_public_manifest_rejects_admin_urls_and_allows_viewform(self):
        self.assertIsNotNone(
            GUARD.public_value_issue(
                "https://docs.google.com/forms/d/example/edit"
            )
        )
        self.assertIsNotNone(
            GUARD.public_value_issue(
                "https://docs.google.com/spreadsheets/d/example/edit"
            )
        )
        self.assertIsNone(
            GUARD.public_value_issue(
                "https://docs.google.com/forms/d/e/example/viewform"
            )
        )


if __name__ == "__main__":
    unittest.main()
