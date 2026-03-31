import unittest
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_list_root(self):
        result = get_files_info("calculator", ".")
        self.assertIsInstance(result, str)
        self.assertFalse(result.startswith("Error:"))

    def test_list_subdir(self):
        result = get_files_info("calculator", "pkg")
        self.assertIsInstance(result, str)
        self.assertFalse(result.startswith("Error:"))

    def test_absolute_path_returns_error(self):
        result = get_files_info("calculator", "/bin")
        self.assertTrue(result.startswith("Error:"))

    def test_parent_traversal_returns_error(self):
        result = get_files_info("calculator", "../")
        self.assertTrue(result.startswith("Error:"))

    def test_not_a_directory_returns_error(self):
        result = get_files_info("calculator", "main.py")
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()
