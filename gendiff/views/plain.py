"""Plain-view module determines new way of rendering Difference object.
`plain view` consists of strings each describing changes made in new version
of file.

Example:
    >>> diff = Difference(file1, file2)
    >>> print(plain_view(diff))
    Property 'common.setting2' was removed
    Property 'common.setting6' was removed
    Property 'common.setting4' was added with value: 'blah blah'
    Property 'common.setting5' was added with value: 'complex value'
    Property 'common.site.base' was removed
    Property 'group1.baz' was changed. From 'bas' to 'bars'
    Property 'group2' was removed
    Property 'group3' was added with value: 'complex value'
"""


from gendiff.diff import Difference
from gendiff.diff import COMMON, NEW, REMOVED, CHANGED


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

    elif diff.status == CHANGED:
        value = "changed. From '{}' to '{}'".format(
            diff.changedfrom.value, diff.value)
        return template.format(value)


def collect_plain(difference) -> list:
    res = []

    for d in difference.contents:
        if isinstance(d.value, Difference) and d.status == COMMON:
            res += collect_plain(d.value)
        else:
            res.append(to_plain(d))
    res = [x for x in res if x]
    return res


def plain_view(difference):
    res = collect_plain(difference)
    return '\n'.join(res)
