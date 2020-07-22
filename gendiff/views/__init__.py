from gendiff.diff import Difference
from gendiff.views import plain, json as jason, default


def render(difference: Difference, format_):
    """Render Difference object.

    Args:
        difference (Difference): Difference object to render.
        format_ (str, optional): Preferred rendering format.
            Choose from ['default', 'plain', 'json'].

    Returns: str
    """

    if format_ == 'plain':
        return plain.plain_view(difference)

    elif format_ == 'json':
        return jason.json_view(difference)

    return default.default_view(difference)
