"""Json-view module consists of methods allowing you to export
`Diff` object contents to json file."""

import json


def render(diff) -> str:
    return json.dumps(diff, indent=4)
