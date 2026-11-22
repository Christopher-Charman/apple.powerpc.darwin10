"""Source-only guard for the PowerPC Apple16X50Serial core target."""

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "src/powerpc/Apple16X50Serial-24/Apple16X50Serial.xcodeproj/project.pbxproj"
SNAPSHOT = ROOT / "src/releases/10.6.8/Apple16X50Serial-24/Apple16X50Serial.xcodeproj/project.pbxproj"
CORE_CONFIGS = (
    "C1D77DC10DD4BCB4001E21DB",  # Development
    "C1D77DC20DD4BCB4001E21DB",  # Deployment
    "C1D77DC30DD4BCB4001E21DB",  # DEBUG
    "C1D77DC40DD4BCB4001E21DB",  # ASSERT
    "C1D77DC50DD4BCB4001E21DB",  # DEBUG & ASSERT
)


def object_text(project, object_id):
    match = re.search(rf"(?ms)^\t\t{object_id} /\* .*?^\t\t\}};", project)
    if not match:
        raise AssertionError(f"missing Xcode project object {object_id}")
    return match.group()


class Apple16X50SerialPPCSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = PROJECT.read_text()

    def test_official_snapshot_is_pristine(self):
        data = SNAPSHOT.read_bytes()
        git_blob = b"blob " + str(len(data)).encode() + b"\0" + data
        self.assertEqual(hashlib.sha1(git_blob).hexdigest(),
                         "ecf43504733f782be1760c9bc8cd75024a4d094e")

    def test_each_core_configuration_selects_ppc(self):
        config_list = object_text(self.project, "C1D77DC00DD4BCB4001E21DB")
        for object_id in CORE_CONFIGS:
            with self.subTest(configuration=object_id):
                self.assertIn(object_id, config_list)
                self.assertRegex(object_text(self.project, object_id),
                                 r"(?m)^\t{4}ARCHS = ppc;$")

    def test_core_does_not_require_acpi_plugin(self):
        core = object_text(self.project, "C1D77DA70DD4BCB4001E21DB")
        self.assertRegex(core, r"dependencies = \(\s*\);")
        self.assertNotIn("C1D77DF00DD4BCB5001E21DB", self.project)
        self.assertNotIn("C1D77DEF0DD4BCB5001E21DB", self.project)
        self.assertIn("C1D77DDB0DD4BCB5001E21DB", self.project)
        embedded = object_text(self.project, "C1D77E290DD4BEC1001E21DB")
        self.assertIn("C1FCFCDC0DD6693E00EEDE4F", embedded)


if __name__ == "__main__":
    unittest.main()
