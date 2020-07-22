from gendiff.diff import Difference
from gendiff.diff import COMMON, NEW, REMOVED


def default_view(difference) -> str:
    return str(difference)


def to_plain(diff) -> str:
    if diff.status == COMMON:
        return
    prop = '.'.join([x.key for x in diff.get_parents()] + [diff.key])
    template = "Property '" + prop + "' was {}"

    if diff.status == NEW:
        value = 'complex value' if isinstance(
            diff.value, Difference) else diff.value
        state = "added with value: '{}'".format(value)
        return template.format(state)

    elif diff.status == REMOVED:
        return template.format('removed')


def plain_view(difference) -> str:
    res = []

    for d in difference.contents:
        if isinstance(d.value, Difference) and d.status == COMMON:
            res += plain_view(d.value)
        else:
            res.append(to_plain(d))
    res = [x for x in res if x]
    return res


def json_view(difference) -> str:
    pass


def render(difference: Difference, format_):
    """Render Difference object.

    Args:
        difference (Difference): Difference object to render.
        format_ (str, optional): Preferred rendering format.
            Choose from ['default', 'plain', 'json'].

    Returns: str
    """

    if format_ == 'plain':
        return plain_view(difference)

    elif format_ == 'json':
        return json_view(difference)

    return default_view(difference)
