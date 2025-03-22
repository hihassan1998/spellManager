#!/usr/bin/env python3
""" Module for testing the class Die """

import unittest
import unittest
from src.trie import Trie
# from src.errors import SearchMiss


class TestTrie(unittest.TestCase):
    """
    Test cases for the Trie class module.
    """

    def test_insertion(self):
        """
        Test inserting a word.
        """
        self.trie = Trie()
        word = "hello"
        self.trie.insert(word)
        self.assertTrue(self.trie.search(word))

    def test_search(self):
        """
        Test searching for a word.
        """
        self.trie = Trie()
        word = "hello"
        self.trie.insert(word)
        self.assertTrue(self.trie.search(word))
        self.assertFalse(self.trie.search("world"))


if __name__ == "__main__":
    unittest.main()
