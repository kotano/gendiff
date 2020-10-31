"""Plain-view module determines new way of rendering `Diff` object.
`plain view` consists of strings each describing changes made in new version
of file.

Example:
    >>> generate_diff(before, after, 'plain')
    Property 'common.setting2' was removed
    Property 'common.setting6' was removed
    Property 'common.setting4' was added with value: 'blah blah'
    Property 'common.setting5' was added with value: 'complex value'
    Property 'common.site.base' was removed
    Property 'group1.baz' was changed. From 'bas' to 'bars'
    Property 'group2' was removed
    Property 'group3' was added with value: 'complex value'
"""


from gendiff import diff


TEMPLATE = "Property '{}' was {}"

status_maps = {
    diff.CHANGED: "changed. From '{}' to '{}'",
    diff.ADDED: "added with value: '{}'",
    diff.DELETED: "removed",
}


def collect_plain(dif, path='') -> list:
    res = []
    for k, v in dif.items():
        status, *values = v
        if status == diff.NESTED:
            res += collect_plain(values[0], "{}{}.".format(path, k))
        elif status == diff.UNCHANGED:
            continue
        else:
            if status == diff.ADDED and isinstance(values[0], dict):
                values = ['complex value']
            res.append(TEMPLATE.format(
                path + k,
                status_maps[status].format(*values)))
    return res


def render(diff) -> str:
    return '\n'.join(collect_plain(diff))
