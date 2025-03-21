import os

class FileManager:
    DIRECTORY = "filestxt"

    @staticmethod
    def get_available_files():
        return [f for f in os.listdir(FileManager.DIRECTORY) if f.endswith(".txt")]

    @staticmethod
    def load_words_from_file(filename):
        path = os.path.join(FileManager.DIRECTORY, filename)
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
