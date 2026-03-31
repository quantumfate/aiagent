import unittest
from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_run_main_no_args(self):
        result = run_python_file("calculator", "main.py")
        self.assertIn("STDOUT:", result)
        self.assertIn("Calculator App", result)

    def test_run_main_with_args(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        self.assertIn("STDOUT:", result)
        self.assertIn('"result": 8', result)

    def test_run_test_file(self):
        result = run_python_file("calculator", "tests.py")
        self.assertIn("STDERR:", result)
        self.assertIn("OK", result)

    def test_parent_traversal_returns_error(self):
        result = run_python_file("calculator", "../main.py")
        self.assertTrue(result.startswith("Error:"))

    def test_nonexistent_file_returns_error(self):
        result = run_python_file("calculator", "nonexistent.py")
        self.assertTrue(result.startswith("Error:"))

    def test_non_python_file_returns_error(self):
        result = run_python_file("calculator", "lorem.txt")
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()
