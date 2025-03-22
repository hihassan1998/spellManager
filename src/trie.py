#!/usr/bin/env python3
"""
This module contains the Trie class, which implements an unordered linked list.
The class provides methods to append, get, set, remove, and manipulate list items.
It also allows support of iteration over the list to skip manual data retrival.
"""
from src.node import Node
from src.errors import SearchMiss, InsertError
from src.file_manager import FileManager


class Trie:
    """
    Constructor for the Trie class.
    Methods:
        insert(word): Adds a word to the Trie.
        search(word): Checks if a word exists.
        remove(word): Deletes a word, raising SearchMiss if not found.
        search_prefix(prefix): Returns words starting with a prefix.
        get_all_words(): Returns all words in the Trie.
        size(): Returns the total word count.
        create_from_file(filename): Creates a Trie from a file.
    """

    def __init__(self):
        """
        Initializes the Trie with an empty root node.
        """
        self.root = Node()

    def insert(self, word: str):
        """
        Inserts a word into the Trie.
        """
        if not word:
            raise InsertError("Cannot insert an empty string into the Trie.")

        word = word.lower()
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end_of_word = True

    def remove(self, word: str):
        """Removes a word from the Trie. Raises SearchMiss if the word is not found."""
        word = word.lower()
        if not self.search(word):
            raise SearchMiss(f"The word '{word}' not found in Trie.")

        _remove(self.root, word, 0)

    def search(self, word: str) -> bool:
        """Checks if a word exists in the Trie. Raises SearchMiss if not found."""
        word = word.lower()
        node = self.root
        for char in word:
            if char not in node.children:
                raise SearchMiss(f"The word '{word}' not found in Trie.")
            node = node.children[char]
        if not node.is_end_of_word:
            raise SearchMiss(f"The word '{word}' not found in Trie.")
        return True

    def search_prefix(self, prefix: str):
        """
        Returns a list of words in the Trie that start with the given prefix.
        """
        prefix = prefix.lower()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return _fetch_words(node, prefix)

    def get_all_words(self):
        """
        Returns a list of all words in the Trie.
        """
        return self.search_prefix("")

    def size(self) -> int:
        """
        Returns the total number of nodes in the trie.
        """
        return _count_words(self.root)

    def search_suffix(self, suffix):
        """
        Searches for all words in the Trie that end with the given suffix.
        Uses post-order traversal to match the suffix.
        """
        suffix = suffix.lower()
        matched_words = []
        self._traverse_and_find_suffix(self.root, "", suffix, matched_words)
        return sorted(matched_words)

    def _traverse_and_find_suffix(self, node, current_word, suffix, matched_words):
        """
        Helper method for recursive post-order traversal.
        It checks if the current_word (built so far) ends with the suffix.
        """
        if node.is_end_of_word:
            if self._ends_with(current_word, suffix):
                matched_words.append(current_word)
        for char, child_node in node.children.items():
            self._traverse_and_find_suffix(
                child_node, current_word + char, suffix, matched_words)

    def _ends_with(self, word, suffix):
        """
        Checks if the word ends with the given suffix by manually comparing characters.
        """
        word_len = len(word)
        suffix_len = len(suffix)
        if word_len < suffix_len:
            return False
        for i in range(suffix_len):
            if word[word_len - suffix_len + i] != suffix[i]:
                return False
        return True

    @classmethod
    def create_from_file(cls, filename):
        """
        Class method to create a Trie instance and populate it with words from a file.
        """
        trie = cls()
        words = FileManager.load_words_from_file(filename)
        for word in words:
            trie.insert(word)
        return trie


# Helper sleeper fucntions

def _remove(node, word, depth):
    """
    Recursively removes a word from the Trie.
    Returns True if the node should be deleted, False otherwise.
    """
    if depth == len(word):
        if not node.is_end_of_word:
            return False
        node.is_end_of_word = False
        return len(node.children) == 0
    char = word[depth]
    if char not in node.children:
        return False
    should_delete = _remove(node.children[char], word, depth + 1)
    if should_delete:
        del node.children[char]
    return not node.is_end_of_word and len(node.children) == 0


def _fetch_words(node, prefix):
    words = []
    if node.is_end_of_word:
        words.append(prefix)
    for char, child in node.children.items():
        words.extend(_fetch_words(child, prefix + char))
    return words


def _count_words(node):
    """
    Counts the total number of words in the Trie.
    Returns the total word count.
    """
    count = 0
    if node.is_end_of_word:
        count += 1
    for child in node.children.values():
        count += _count_words(child)
    return count
