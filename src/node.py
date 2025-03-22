#!/usr/bin/env python3
"""
This module defines the Node class.
"""


class Node():
    """
    Represents a node in a Trie data structure.

    Attributes:
        children (dict): A dictionary to hold child nodes.
        is_end_of_word (bool): Flag indicating if the node is the end of a word.
    """

    def __init__(self):
        """
          Initializes a new node with an empty children dictionary and is_end_of_word set to False.
        """
        self.children = {}
        self.is_end_of_word = False