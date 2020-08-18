"""Json-view module consists of methods allowing you to export
`Diff` object contents to json file."""

import json

from gendiff.diff import Diff


def get_json_string(diff: Diff, indent=4) -> str:
    """Return json string from difference object."""

    def call_to_dict(obj):
        """Call object's to_dict() function to get dictionary in case
        'json.dumps' can not serialize object's contents."""
        return obj.to_dict()

    json_string = json.dumps(
        diff.__dict__,
        indent=indent,
        default=call_to_dict,
        check_circular=True
    )

    return json_string


def render(diff: Diff) -> str:
    return get_json_string(diff)
