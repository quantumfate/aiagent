import unittest
import os
from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):
    def test_write_root(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        self.assertTrue(result.startswith("Successfully wrote"))
        self.assertIn("28 characters written", result)

    def test_write_subdir(self):
        result = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        self.assertTrue(result.startswith("Successfully wrote"))
        self.assertIn("26 characters written", result)

    def test_outside_working_dir_returns_error(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        self.assertTrue(result.startswith("Error:"))

    def tearDown(self):
        for path in [
            "calculator/lorem.txt",
            "calculator/pkg/morelorem.txt",
        ]:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
