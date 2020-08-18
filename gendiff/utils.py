"""Utilities module for gendiff project."""
import json
from pathlib import Path

import yaml


BASEDIR: Path = Path(__file__).parent.parent


def list_package(path):
    """List python package.

    Args:
        path (str): Path to package, starting from basedir/cwd.

    Returns:
        list: List of available modules without __init__.
    """
    res = []
    p = BASEDIR / path
    for m in p.glob('*.py'):
        if not m.name.startswith('__'):
            res.append(m.stem)
    return res


def load(path):
    """Return python dictionary from file.

    Args:
        path (str): Path to file.

    Returns: dict
    """
    data = None
    with open(path) as f:
        ext = path.split('.')[-1]
        if ext == 'yml':
            data = yaml.safe_load(f)
        elif ext == 'json':
            data = json.load(f)
    return data


def safe_read(filename, **kwargs) -> str:
    """Read file.

    Args:
        filename (str): Path to file.

    Returns:
        str: File contents.
    """
    with open(filename, **kwargs) as f:
        return f.read()
