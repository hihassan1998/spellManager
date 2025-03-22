#!/usr/bin/env python3
"""
This module contains the Error handling classs for the Nodes at errorneous searches.
"""


class SearchMiss(Exception):
    """Exception raised when a search fails in the Trie."""


class InsertError(Exception):
    """Exception raised when trying to insert an invalid word into the Trie."""
