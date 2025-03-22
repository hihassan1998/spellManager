#!/usr/bin/env python3
"""
This module contains the Error handling classs for the Nodes at errorneous searches.
"""


class SearchMiss(Exception):
    """Exception raised when a search operation fails in the Trie."""
