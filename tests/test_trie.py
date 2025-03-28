#!/usr/bin/env python3
""" Module for testing the class of Trie """

import unittest
from src.trie import Trie
from src.errors import SearchMiss, InsertError


class TestTrie(unittest.TestCase):
    """
    Test cases for the Trie class module.
    """

    def test_insert_and_search_word(self):
        """Test if a word is correctly inserted and searched in the Trie"""
        trie = Trie()
        trie.add_word('hello')

        self.assertTrue(trie.search('hello'),
                        "Word 'hello' found in the Trie")

        with self.assertRaises(SearchMiss):
            trie.search('hell')

    def test_insert_empty_word(self):
        """Test inserting an empty string as a word"""
        trie = Trie()
        with self.assertRaises(InsertError):
            trie.add_word('')

    def test_remove_existing_word(self):
        """Test if a word can be removed from the Trie"""
        trie = Trie()
        trie.add_word('hello')
        self.assertTrue(trie.search('hello'),
                        "The word 'hello' found in the Trie")
        trie.remove('hello')
        with self.assertRaises(SearchMiss):
            trie.search('hello')

    def test_remove_empty_word(self):
        """Test if attempting to remove an empty string raises a SearchMiss error"""
        trie = Trie()

        with self.assertRaises(SearchMiss):
            trie.remove('')

    def test_get_all_words(self):
        """Test if all words can be retrieved from the Trie"""
        trie = Trie()
        trie.add_word('hello')
        trie.add_word('world')

        all_words = trie.get_all_words()
        self.assertEqual(sorted(all_words), sorted(
            ['hello', 'world']))

    def test_size(self):
        """Test if size function returns correct number of words"""
        trie = Trie()
        trie.add_word('hello')
        trie.add_word('world')

        self.assertEqual(trie.size(), 2)

    def test_create_from_file(self):
        """Test if creating a Trie from a file works correctly"""
        trie = Trie.create_from_file('tiny_dictionary.txt')

        self.assertTrue(trie.search(
            'the'), "The word 'the' found in the Trie created from the given file")

    def test_prefix_search(self):
        """Test if prefix search works correctly"""
        trie = Trie()
        trie.add_word('hello')
        trie.add_word('hell')
        trie.add_word('helium')

        results = trie.prefix_search('hel')
        self.assertEqual((results), ['hell', 'hello', 'helium'])

    def test_search_suffix(self):
        """Test if suffix search works correctly"""
        trie = Trie()
        trie.add_word('hello')
        trie.add_word('world')

        suffix_words = trie.suffix_search('llo')
        self.assertEqual(suffix_words, ['hello'])

        suffix_words = trie.suffix_search('xyz')
        self.assertEqual(suffix_words, [])


if __name__ == "__main__":
    unittest.main()
