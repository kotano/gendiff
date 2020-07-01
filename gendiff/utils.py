"""Utilities module for gendiff project."""
import json

import yaml


def open_file(path):
    """Return python object from file.

    Args:
        path (str): Path to file.

    Returns:
        any: Returns corresponding python object,
            depending on file contents.
    """
    data = None
    with open(path) as f:
        ext = path.split('.')[-1]
        if ext == 'yml':
            data = yaml.safe_load(f)
        elif ext == 'json':
            data = json.load(f)
    return data


def convert_to_tuple(d: dict):
    """Recursively convert dict key-value pairs to tuple.

    Args:
        d (dict): Dictionary to convert.

    Returns:
        tuple: Tuple in (key, value) format.
    """
    res = {}
    for k, v in d.items():
        if isinstance(v, dict):
            res[k] = convert_to_tuple(v)
        else:
            res[k] = v
    return tuple(res.items())
