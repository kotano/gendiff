"""Gendiff project main module.

This module contains main logics for `Gendiff` project.


TODO:
    * Consider refactoring
        * Remove extra variables
"""

from gendiff.diff import Difference
from gendiff.utils import open_file
from gendiff.views import render


def generate_diff(file1, file2, format_='default'):
    """Generate difference between two files.

    Args:
        file1 (str): Path to `old` file.
        file2 (str): Path to `new` file.
        format_ (str): Difference output format
            choose from ['default', 'plain', 'json']

    Returns:
        str: Json-like stri
    """

    data1 = open_file(file1)
    data2 = open_file(file2)

    diff = Difference(data1, data2)

    return render(diff, format_)
