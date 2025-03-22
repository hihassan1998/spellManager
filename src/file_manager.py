"""
FileManager module for handling text file operations.

This module provides utility functions to list available text files
and load words from a selected file.
"""
import os


class FileManager:
    """Manages file operations for loading words from text files."""
    DIRECTORY = "filestxt"

    @staticmethod
    def get_available_files():
        """Return a list of available .txt files in the directory."""
        files = os.listdir(FileManager.DIRECTORY)
        txt_files = []
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(file)
        return txt_files

    @staticmethod
    def load_words_from_file(filename):
        """Load words from a specified text file and return them as a list."""
        path = os.path.join(FileManager.DIRECTORY, filename)
        with open(path, "r", encoding="utf-8") as file:
            words = []
            for line in file:
                words.append(line.strip())
        return words
