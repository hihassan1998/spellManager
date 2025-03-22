import os


class FileManager:
    DIRECTORY = "filestxt"

    @staticmethod
    def get_available_files():
        files = os.listdir(FileManager.DIRECTORY)
        txt_files = []
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(file)
        return txt_files

    @staticmethod
    def load_words_from_file(filename):
        path = os.path.join(FileManager.DIRECTORY, filename)
        with open(path, "r", encoding="utf-8") as file:
            words = []
            for line in file:
                words.append(line.strip())
        return words
