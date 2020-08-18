"""Plain-view module determines new way of rendering `Diff` object.
`plain view` consists of strings each describing changes made in new version
of file.

Example:
    >>> diff = Diff(file1, file2)
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


from gendiff.diff import Diff
from gendiff.diff import COMMON, NEW, REMOVED, MODIFIED


def to_plain(change) -> str:
    if change.status == COMMON:
        return

    prop = '.'.join([x.key for x in change.get_parents()] + [change.key])
    template = "Property '" + prop + "' was {}"

    if change.status == NEW:
        value = 'complex value' if isinstance(
            change.value, Diff) else change.value
        state = "added with value: '{}'".format(value)
        return template.format(state)

    elif change.status == REMOVED:
        return template.format('removed')

    elif change.status == MODIFIED:
        value = "changed. From '{}' to '{}'".format(
            change.changedfrom.value, change.value)
        return template.format(value)


def collect_plain(diff) -> list:
    res = []

    for d in diff.contents:
        if isinstance(d.value, Diff) and d.status == COMMON:
            res += collect_plain(d.value)
        else:
            res.append(to_plain(d))
    res = [x for x in res if x]
    return res


def render(diff):
    res = collect_plain(diff)
    return '\n'.join(res)
