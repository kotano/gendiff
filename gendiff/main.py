"""Gendiff project main module.

This module contains main logics for `Gendiff` project.
"""
import json
from pathlib import Path

import yaml

from gendiff.diff import get_diff
from gendiff.views import render_view


BASEDIR: Path = Path(__file__).parent.parent


def load(path) -> dict:
    """Return python dictionary from file.

    Args:
        path (str): Path to file.

    Returns: dict
    """
    data = None
    fname = Path(path).resolve()
    with open(fname) as f:
        if fname.suffix in ['.yml', '.yaml']:
            data = yaml.safe_load(f)
        elif fname.suffix == '.json':
            data = json.load(f)
    return data


def generate_diff(file1, file2, format_='stylish') -> str:
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
    diff = get_diff(data1, data2)
    return render_view(diff, format_)
