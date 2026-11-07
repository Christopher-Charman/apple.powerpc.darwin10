import unittest
from tools.validate_experiment import validate

DIGEST = "a" * 64

def receipt():
    return {
        "run_id": "a5-g4-001",
        "target": "10.6.8 PPC Alpha 5",
        "hypothesis": "specific symbol mismatch",
        "prediction": "import fails",
        "falsifier": "import succeeds",
        "procedure": "record dyld import trace",
        "source": {"identifier": "source revision", "sha256": DIGEST},
        "toolchain": {"identifier": "PPC toolchain", "sha256": DIGEST},
        "image": {"identifier": "image UUID", "sha256": DIGEST},
        "hardware": {"model": "PowerBook5,6", "boot_rom": "4.9.1f3",
                     "cpu": "PowerPC G4", "ram_bytes": 2147483648},
        "results": {"verdict": "planned", "observations": [], "artifacts": []},
        "evidence_class": "historical",
    }

class ExperimentContractTests(unittest.TestCase):
    def test_valid_planned(self):
        self.assertEqual(validate(receipt()), [])

    def test_valid_negative_result(self):
        x = receipt()
        x["results"]["verdict"] = "falsified"
        x["results"]["observations"] = ["symbol resolved"]
        self.assertEqual(validate(x), [])

    def test_reject_missing_identity(self):
        x = receipt()
        del x["image"]["sha256"]
        self.assertTrue(any("image.sha256" in e for e in validate(x)))

    def test_reject_unobserved_terminal_verdict(self):
        x = receipt()
        x["results"]["verdict"] = "passed"
        self.assertIn("terminal verdict requires at least one observation", validate(x))

    def test_reject_unverified_planned(self):
        x = receipt()
        x["evidence_class"] = "live_verified"
        self.assertIn("planned experiment cannot be live_verified", validate(x))

    def test_malformed_results_no_crash(self):
        x = receipt()
        x["results"] = None
        x["evidence_class"] = "live_verified"
        self.assertIn("results must be an object", validate(x))

    def test_reject_unhashable_verdict(self):
        x = receipt()
        x["results"]["verdict"] = []
        self.assertTrue(validate(x))

    def test_reject_unhashable_evidence_class(self):
        x = receipt()
        x["evidence_class"] = []
        self.assertTrue(validate(x))

    def test_reject_boolean_ram(self):
        x = receipt()
        x["hardware"]["ram_bytes"] = True
        self.assertTrue(validate(x))

if __name__ == "__main__":
    unittest.main()
