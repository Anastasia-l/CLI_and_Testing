import unittest
import os
from unittest.mock import patch
import tempfile
import shutil
import file_manager_functions


class TestCopyFile(unittest.TestCase):
    @patch('os.path.isfile')
    @patch('shutil.copy2')
    def test_copy_file_success(self, mock_copy2, mock_isfile):
        mock_isfile.return_value = True
        file_manager_functions.copy_file('test_file.txt', '/mock/directory')

        mock_isfile.assert_called_with('test_file.txt')
        mock_copy2.assert_called_with('test_file.txt', '/mock/directory')


class TestRemovingFunction(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_directory"
        self.test_file = "test_file.txt"
        os.makedirs(self.test_dir)
        with open(os.path.join(self.test_dir, self.test_file), 'w') as f:
            f.write("This a test file to test my removing function")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_file_deletion(self):
        file_manager_functions.removing(self.test_file, self.test_dir)

        self.assertFalse(os.path.exists(os.path.join(self.test_dir, self.test_file)))

    def test_directory_deletion(self):
        file_manager_functions.removing(self.test_file,
                                        self.test_dir)  # First delelte the file, then delete a directory
        file_manager_functions.removing("", self.test_dir)

        self.assertFalse(os.path.exists(self.test_dir))

    def test_nonexistent_file(self):
        # Call the function with non existent file to check if it works correctly
        with patch("builtins.print") as m:  # Mock the print function
            file_manager_functions.removing("nonexist_file.txt", self.test_dir)

        m.assert_called_with('The file was not found or doesn`t exist!')

    def test_nonexistent_directory(self):
        # Call the function with non existent directory to check if everything works correctly
        with patch("builtins.print") as m:
            file_manager_functions.removing("any_file.txt", "nonexistent_directory")

        m.assert_called_with("The directory was not found or doesn`t exist")


class TestCountingFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_directory"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))  # Remove all subdirectories
            os.rmdir(self.test_dir)  # Remove the main directory

    def test_empty_directory(self):
        with patch('builtins.print') as m:
            file_manager_functions.counting_files(self.test_dir)
            m.assert_called_with('The amount of files in the directory: test_directory: 0')

    def test_directory_with_files(self):
        # Create some files in the directory
        with open(os.path.join(self.test_dir, "file_1.txt"), "w") as f:
            f.write("This is file 1")
        with open(os.path.join(self.test_dir, "file_2.txt"), "w") as f:
            f.write("This is file 2")

        with patch('builtins.print') as m:
            file_manager_functions.counting_files(self.test_dir)
            m.assert_called_with('The amount of files in the directory: test_directory: 2')

    def test_directory_with_subdirectories_and_files(self):
        sub_dir = os.path.join(self.test_dir, "sub_directory")
        os.makedirs(sub_dir)

        with open(os.path.join(self.test_dir, "file1.txt"), "w") as f:
            f.write("This is file 1")
        with open(os.path.join(self.test_dir, "file2.txt"), "w") as f:
            f.write("This is file 2")
        with open(os.path.join(self.test_dir, "file3.txt"), "w") as f:
            f.write("This is file 3")

        with patch("builtins.print") as m:
            file_manager_functions.counting_files(self.test_dir)

        m.assert_called_with('The amount of files in the directory: test_directory: 3')

    def test_nonexistent_directory(self):
        non_existent_directory = "non_existent_dir"

        with patch("builtins.print") as m:
            file_manager_functions.counting_files(non_existent_directory)

        m.assert_called_with('The amount of files in the directory: non_existent_dir: 0')


class TestFindMatchingFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()  # Create a temporary directory

        # Create some test files
        self.files = {
            'test1.txt': "Test file N1",
            'test2.doc': "Test file N2",
            'test3.txt': "Test file N3",
            'image.png': "Test file N4"
        }

        for filename, content in self.files.items():
            with open(os.path.join(self.test_dir, filename), "w") as f:
                f.write(content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)  # Remove the temporary directory after the test

    def test_finding_matching_files(self):
        pattern = r'\.txt$'
        result = file_manager_functions.find_matching_files(self.test_dir, pattern)

        # Expected files
        expected = [
            os.path.join(self.test_dir, 'test1.txt'),
            os.path.join(self.test_dir, 'test3.txt')
        ]

        # Assert the results match the expected
        self.assertEqual(sorted(result), sorted(expected))

    def test_find_mathincg_no_match(self):
        pattern = r'\.pdf'
        result = file_manager_functions.find_matching_files(self.test_dir, pattern)

        # Assert that there are no matching files
        self.assertEqual(result, [])


class TestDateFileFunction(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = "temp_test_file.txt"
        with open(self.temp_file, "w") as f:
            f.write("This is a test file")

    def tearDown(self):
        # Clean up any files created during the test
        for file in os.listdir():
            if file.startswith("temp_test_file"):
                os.remove(file)

    @patch("os.path.getctime")
    def test_get_file_birthday(self, mock_getctime):
        # Mock the creation time to return a fixed timestamp
        mock_timestamp = 1739717578
        expected_date = "2025-02-16"
        mock_getctime.return_value = mock_timestamp

        # Call the function
        result = file_manager_functions.get_file_birthday(self.temp_file)

        # Assert the result is in the correct format
        self.assertEqual(result, "2025-02-16")

    def test_get_file_birthday_invalid_file(self):
        invalid_path = "non_existent_file.txt"

        # Assert that the function raises an exception
        with self.assertRaises(FileNotFoundError):
            file_manager_functions.get_file_birthday(invalid_path)


class TestRenameFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, 'w') as f:
            f.write("This is a test file")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.test_dir)

    @patch("builtins.print")
    @patch("file_manager_functions.get_file_birthday")
    def test_rename_file(self, mock_get_birthday, mock_print):
        mock_get_birthday.return_value = "2025-02-16"
        file_manager_functions.rename_file_with_date(self.test_file)
        basename, extension = os.path.splitext(os.path.basename(self.test_file))
        expected_new_name = f"{basename}_2025-02-16{extension}"
        expected_new_path = os.path.join(os.path.dirname(self.test_file), expected_new_name)
        self.assertFalse(os.path.exists(self.test_file))
        self.assertTrue(os.path.exists(expected_new_path))
        expected_output = f"Renamed: {os.path.basename(self.test_file)} -> {expected_new_name}"
        mock_print.assert_called_once_with(expected_output)

    def test_rename_file_nonexisting(self):
        nonexisting_file = os.path.join(self.test_dir, "nonexistent.txt")
        with self.assertRaises(FileNotFoundError):
            file_manager_functions.rename_file_with_date(nonexisting_file)


class TestProcessFolder(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.file1 = os.path.join(self.test_dir, "Test_file1.txt")
        self.file2 = os.path.join(self.test_dir, "Test_file2.doc")
        self.subdir = os.path.join(self.test_dir, "subdir")
        self.file3 = os.path.join(self.subdir, "Test_file2.txt")

        os.makedirs(self.subdir)
        with open(self.file1, "w") as f:
            f.write("Test content")
        with open(self.file2, "w") as f:
            f.write("Test file 2 content")
        with open(self.file3, "w") as f:
            f.write("Test File 3")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    shutil.rmtree(os.path.join(root, name))
            os.rmdir(self.test_dir)

    @patch("file_manager_functions.rename_file_with_date")
    def test_process_folder_recursively(self, mock_rename_file):
        file_manager_functions.process_folder(self.test_dir, recursive=True)
        expected_output = [self.file1, self.file2, self.file3]
        for file in expected_output:
            mock_rename_file.assert_any_call(file)

    @patch("file_manager_functions.rename_file_with_date")
    def test_process_folder_non_recursively(self, mock_rename_file):
        file_manager_functions.process_folder(self.test_dir, recursive=False)
        expected_output = [self.file1, self.file2]
        for file in expected_output:
            mock_rename_file.assert_any_call(file)


if __name__ == "__main__":
    unittest.main()
