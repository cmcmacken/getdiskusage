from getdiskusage import get_du_binary, parse_output
from unittest.mock import patch
import unittest
import json


class GetDuTest(unittest.TestCase):

    @patch("shutil.which")
    @patch("platform.system")
    def test_windows(self, mock_platform, mock_which):
        mock_platform.return_value = "Windows"
        mock_which.return_value = None

        with self.assertRaises(RuntimeError):
            get_du_binary()

    @patch("shutil.which")
    @patch("platform.system")
    def test_osx(self, mock_platform, mock_which):
        mock_platform.return_value = "Darwin"
        mock_which.return_value = "/usr/bin/gdu"

        du_name = get_du_binary()
        self.assertEqual(du_name, "gdu")

    @patch("shutil.which")
    @patch("platform.system")
    def test_linux(self, mock_platform, mock_which):
        mock_platform.return_value = "Linux"
        mock_which.return_value = "/usr/bin/du"

        du_name = get_du_binary()
        self.assertEqual(du_name, "du")

    @patch("shutil.which")
    @patch("platform.system")
    def test_du_not_present(self, mock_platform, mock_which):
        mock_platform.return_value = "Linux"
        mock_which.return_value = False

        with self.assertRaises(FileNotFoundError):
            get_du_binary()


class ParseOutputTestCase(unittest.TestCase):
    def test_sane_output(self):
        sample_output = "824	/var/log/fsck_apfs_error.log\n17015	/var/log/daily.out\n0	/var/log/appfirewall.log\n43147246	/var/log"""

        fake_result = type("obj", (object,), {"stdout" : sample_output})
        output = parse_output(fake_result)

        # rather than asserting everything is equal just check a few things
        json_output = json.loads(output)

        self.assertEqual(len(json_output["files"]), 4)
        self.assertIn({"/var/log/daily.out": "17015"}, json_output["files"])

    def test_malformed_output(self):
        sample_output = "824/var/log/fsck_apfs_error.log\n17015	/var/log/daily.out\n0	/var/log/appfirewall.log\n43147246	/var/log"""

        fake_result = type("obj", (object,), {"stdout" : sample_output})

        with self.assertRaises(ValueError):
            parse_output(fake_result)

if __name__ == '__main__':
    unittest.main()