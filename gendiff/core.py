"""Gendiff project main module.

This module contains main logics for `Gendiff` project.
"""

from gendiff.diff import Difference
from gendiff.utils import safe_load
from gendiff.views import render


def generate_diff(file1, file2, format_='default'):
    """Generate difference between two files.

    Args:
        file1 (str): Path to `old` file.
        file2 (str): Path to `new` file.
        format_ (str): Difference output format
            choose from ['default', 'plain', 'json']

    Returns:
        str: Json-like string
    """

    data1 = safe_load(file1)
    data2 = safe_load(file2)

    diff = Difference(data1, data2)

    return render(diff, format_)
