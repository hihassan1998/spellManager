#!/usr/bin/env python3
""" Module for testing the class of FileManager """
import unittest
from unittest.mock import patch
from src.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    """
    Test cases for the FileManager class module.
    """

    @patch("os.listdir")
    def test_get_available_files(self, mock_listdir):
        """Test if the method returns a list of available .txt files"""
        mock_listdir.return_value = ["file1.txt",
                                     "file2.txt", "image.png", "file3.txt"]

        expected_files = ["file1.txt", "file2.txt", "file3.txt"]

        available_files = FileManager.get_available_files()

        self.assertEqual(available_files, expected_files)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_words_from_file_file_not_found(self, _):
        """Test if FileNotFoundError is raised when the file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            FileManager.load_words_from_file("invisible-file.txt")


if __name__ == "__main__":
    unittest.main()
