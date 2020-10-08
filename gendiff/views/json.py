"""Json-view module consists of methods allowing you to export
`Diff` object contents to json file."""

import json

from gendiff.diff import Diff


def get_json_string(diff: Diff, indent=4) -> str:
    """Return json string from difference object."""

    def call_serialize(obj):
        return obj.serialize()

    json_string = json.dumps(
        diff.serialize(),
        indent=indent,
        default=call_serialize,
    )

    return json_string


def render(diff: Diff) -> str:
    return get_json_string(diff)
