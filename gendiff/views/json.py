"""Json-view module consists of methods allowing you to export
Difference object contents to json file."""

import json

from gendiff.diff import Difference


def json_view(difference: Difference) -> str:
    return get_json_string(difference)


def get_json_string(difference: Difference, indent=4) -> str:
    """Return json string from difference object."""

    def call_to_dict(obj):
        """Call object's to_dict() function to get dictionary in case
        'json.dumps' can not serialize object's contents."""
        return obj.to_dict()

    json_string = json.dumps(
        difference.__dict__,
        indent=indent,
        default=call_to_dict,
        check_circular=True
    )

    return json_string
