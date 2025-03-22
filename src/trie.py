#!/usr/bin/env python3
"""
This module contains the Trie class, which implements an unordered linked list.
The class provides methods to append, get, set, remove, and manipulate list items.
It also allows support of iteration over the list to skip manual data retrival.
"""
from src.node import Node
from src.errors import MissingIndex, MissingValue


class Trie:
    """
    Represents an unordered list implemented as a linked list.

    Attributes:
        head (Node): The first node in the list. It stores data and points to the next node.
    """

    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end_of_word = True

    def remove(self, word: str):
        def _remove(node, word, depth):
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

        _remove(self.root, word, 0)

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def search_prefix(self, prefix: str):
        def _dfs(node, prefix):
            words = []
            if node.is_end_of_word:
                words.append(prefix)
            for char, child in node.children.items():
                words.extend(_dfs(child, prefix + char))
            return words
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return _dfs(node, prefix)

    def get_all_words(self):
        return self.search_prefix("")

    def size(self) -> int:
        """
        Returns the total number of nodes in the trie.

        Returns:
            int: The total number of nodes.
        """
        def _count_words(node):
            count = 0
            if node.is_end_of_word:
                count += 1
            for child in node.children.values():
                count += _count_words(child)
            return count

        return _count_words(self.root)
