#!/usr/bin/env python3
"""
This module contains the Node class and the Error handling classes for the Nodes at indexes.
"""


class Node():
    """
    Node class
    """

    def __init__(self):
        """
        Initialize object with the data and set next to None.
        next will be assigned later when new data needs to be added.
        """
        self.children = {}
        self.is_end_of_word = False
