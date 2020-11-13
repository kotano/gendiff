"""Views package.

Use this module to add new views into the program.
"""
from gendiff.views import plain, json as jason, stylish


VIEWS = {
    'stylish': stylish,
    'plain': plain,
    'json': jason,
}


def render_view(diff, format_):
    """Render `Diff` object.

    Args:
        diff (Diff): `Diff` object to render.
        format_ (str, optional): Preferred rendering format.

    Returns: str
    """
    view = VIEWS.get(format_)
    return view.render(diff)
