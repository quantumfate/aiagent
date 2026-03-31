import unittest
from functions.get_file_content import get_file_content


class TestGetFileContent(unittest.TestCase):
    def test_get_main(self):
        result = get_file_content("calculator", "main.py")
        self.assertIsInstance(result, str)
        self.assertFalse(result.startswith("Error:"))

    def test_get_nested(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        self.assertIsInstance(result, str)
        self.assertFalse(result.startswith("Error:"))

    def test_absolute_path_returns_error(self):
        result = get_file_content("calculator", "/bin/cat")
        self.assertTrue(result.startswith("Error:"))

    def test_nonexistent_file_returns_error(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()
