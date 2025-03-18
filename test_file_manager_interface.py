import unittest
from unittest.mock import patch
import argparse
from file_manager_interface import handle_command, main


class TestFileManagerInterface(unittest.TestCase):

    @patch("file_manager_functions.copy_file")
    def test_handle_command_copy(self, mock_copy_file):
        args = argparse.Namespace(command="copy", filename="test.txt", directory_name="test_dir")
        handle_command(args)
        mock_copy_file.assert_called_once_with("test.txt", "test_dir")

    @patch("file_manager_functions.removing")
    def test_handle_command_removing(self, mock_removing):
        args = argparse.Namespace(command="remove", filename="test.txt", directory_name="test_dir")
        handle_command(args)
        mock_removing.assert_called_once_with("test.txt", "test_dir")

    @patch("file_manager_functions.counting_files")
    def test_counting_files(self, mock_counting_files):
        args = argparse.Namespace(command="count", directory_name="test_dir")
        handle_command(args)
        mock_counting_files.assert_called_once_with("test_dir")

    @patch("file_manager_functions.find_matching_files")
    def test_find_matching_files(self, mock_find_matching_files):
        args = argparse.Namespace(command="find", directory="test_dir", pattern="\.txt")
        handle_command(args)
        mock_find_matching_files.assert_called_once_with("test_dir", "\.txt")

    @patch("file_manager_functions.get_file_birthday")
    def test_get_file_birthday(self, mock_get_file_birthday):
        args = argparse.Namespace(command="creation_date", full_path="full_path_to_test.txt")
        handle_command(args)
        mock_get_file_birthday.assert_called_once_with("full_path_to_test.txt")

    @patch("os.path.exists", return_value=False)
    @patch("builtins.print")
    def test_folder_does_not_exist(self, mock_print, mock_exists):
        args = argparse.Namespace(command="rename_folder_with_date", folder_path="nonexistent_folder")
        handle_command(args)
        mock_print.assert_called_once_with("Sorry, but this folder doesn`t exist!")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.input", return_value='no')
    @patch("builtins.print")
    def test_user_cancel_renaming(self, mock_print, mock_input, mock_exists):
        args = argparse.Namespace(command="rename_folder_with_date", folder_path="test_folder")
        handle_command(args)
        mock_print.assert_called_once_with("Cancelled by user")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.input", return_value="yes")
    @patch("file_manager_functions.rename_file_with_date")
    @patch("builtins.print")
    def test_renaming_folder_recursively(self, mock_input, mock_exists, mock_print, mock_rename):
        args = argparse.Namespace(command="rename_folder_with_date", folder_path="test_folder")
        handle_command(args)
        mock_rename.assert_called_once_with("test_folder")

    @patch("os.path.exists", return_value=True)
    @patch("file_manager_functions.process_folder")
    @patch("builtins.input", return_value="yes")
    @patch("builtins.print")
    def test_renaming_all_files_recursively(self, mock_print, mock_input, mock_process_folder, mock_exists):
        args = argparse.Namespace(command="rename_files_with_date", folder_path="test_path", recursive=True)
        handle_command(args)
        mock_process_folder.assert_called_once_with("test_path", recursive=True)
        mock_print.assert_called_once_with(f"All the files in test_path were succesfully renamed!")

    @patch("os.path.exists", return_value=True)
    @patch("file_manager_functions.process_folder")
    @patch("builtins.input", return_value="yes")
    @patch("builtins.print")
    def test_renaming_all_files_non_recursively(self, mock_print, mock_input, mock_process_folder, mock_exists):
        args = argparse.Namespace(command="rename_files_with_date", folder_path="test_path", recursive=False)
        handle_command(args)
        mock_process_folder.assert_called_once_with("test_path", recursive=False)
        mock_print.assert_called_once_with(f"All the files in test_path were succesfully renamed!")

    @patch("file_manager_functions.analyzing_directory")
    def test_analyzing_sizes(self, mock_analyze):
        args = argparse.Namespace(command="analyze", directory_name="test_dir")
        handle_command(args)
        mock_analyze.assert_called_once_with("test_dir")


if __name__ == "__main__":
    unittest.main()