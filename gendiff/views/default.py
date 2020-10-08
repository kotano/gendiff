from gendiff import diff

sign_maps = {
    diff.COMMON: ' ',
    diff.NEW: '+',
    diff.REMOVED: '-',
    diff.MODIFIED: 'm'
}


def render(dif) -> str:
    return draw_diff(dif)


def draw_diff(dif) -> str:
    # Indentation for closing bracket.
    depth = dif.level + 1 if dif.parent else dif.level
    indent = depth * 2 * ' '
    contents = '\n'.join([draw_change(x) for x in dif.contents])
    template = (
        "{{\n"
        "{contents}\n"
        "{indent}""}}"
    )
    res = template.format(
        contents=contents,
        indent=indent
    )
    return res


def draw_change(change) -> str:
    template = '{}{} {}: {}'
    indent = change.level * 2 * ' '
    status = change.status
    value = change.value
    if isinstance(value, diff.Diff):
        value = draw_diff(change.value)

    if change.status == diff.MODIFIED:
        # Add previous diff on top of current
        template = '{}\n{}'.format(draw_change(change.changedfrom), template)
        status = diff.NEW

    res = template.format(
        indent,
        sign_maps[status],  # Change status text to symbol.
        change.key,
        value
    )

    return res
