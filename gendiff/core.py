"""Gendiff project main script.

This module contains main logics for `Gendiff` project.


TODO:
    * Consider refactoring
        * Remove extra variables
"""

from gendiff.utils import open_file
from gendiff.diff import Difference


def generate_diff(file1, file2):
    """Generate difference between two files.

    Args:
        file1 (str): Path to `old` file.
        file2 (str): Path to `new` file.

    Returns:
        str: Json-like string.
    """

    data1 = open_file(file1)
    data2 = open_file(file2)

    diff = Difference(data1, data2)
    return str(diff)
