"""Gendiff project main module.

This module contains main logics for `Gendiff` project.
"""

from gendiff.diff import Diff
from gendiff.utils import load
from gendiff.views import render_view


def generate_diff(file1, file2, format_='default'):
    """Generate difference between two files.

    Args:
        file1 (str): Path to `old` file.
        file2 (str): Path to `new` file.
        format_ (str): `Diff` output format
            choose one from views package.

    Returns:
        str: Json-like string
    """

    data1 = load(file1)
    data2 = load(file2)

    diff = Diff(data1, data2)

    return render_view(diff, format_)
