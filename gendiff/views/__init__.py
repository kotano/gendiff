"""Views package.

Use this module to add new views into the program.
"""
from gendiff.diff import Difference
from gendiff.views import plain, json as jason, default


def render(difference: Difference, format_):
    """Render Difference object.

    Args:
        difference (Difference): Difference object to render.
        format_ (str, optional): Preferred rendering format.

    Returns: str
    """
    if not format_:
        return default.default_view(difference)

    elif format_ == 'plain':
        return plain.plain_view(difference)

    elif format_ == 'json':
        return jason.json_view(difference)

    print('Unsupported format. Using default one.')
    return default.default_view(difference)
