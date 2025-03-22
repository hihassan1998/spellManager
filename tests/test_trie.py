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

    def test_insert_and_search(self):
        """
        Test inserting a word and then searching for it.
        """
        self.trie = Trie()
        word = "hello"
        self.trie.insert(word)
        self.assertTrue(self.trie.search(word))
        self.assertFalse(self.trie.search("world"))

if __name__ == "__main__":
    unittest.main()
