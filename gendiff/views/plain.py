from gendiff.diff import Difference
from gendiff.diff import COMMON, NEW, REMOVED, CHANGED


def to_plain(diff) -> str:
    if diff.status == COMMON:
        return ''

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

    return ''


def collect_plain(difference) -> str:
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
