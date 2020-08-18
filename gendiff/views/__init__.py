"""Views package.

Use this module to add new views into the program.
"""
from gendiff.diff import Diff
from gendiff.views import plain, json as jason, default


VIEWS = {
    'default': default,
    'plain': plain,
    'json': jason,
}


def render_view(diff: Diff, format_):
    """Render `Diff` object.

    Args:
        diff (Diff): `Diff` object to render.
        format_ (str, optional): Preferred rendering format.

    Returns: str
    """
    if format_ not in VIEWS:
        return 'Unsupported format.'
    view = VIEWS.get(format_)
    return view.render(diff)
