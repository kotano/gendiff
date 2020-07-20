"""Difference objects.

This module contains classes to work with differences.

TODO:
    * Remove extra levels in definitions
    * Implement nested dicts handling
"""

STATUS = {
    'COMMON': ' ',
    'NEW': '+',
    'REMOVED': '-',
}


def mark_diff(item, level, status=STATUS['COMMON']):
    res = []
    for k, v in item:
        res.append(
            Diff(status, level, k, v)  # NOTE
        )
    return res

# def find_common()


class Diff(object):
    def __init__(self, status=' ', level=1, key=None, value=None):
        self.level = level
        self.sign = status
        self.key = key
        self.value = value

    def __repr__(self):
        indent = self.level * '  '
        rep = '{}{} {} : {}'.format(
            indent,
            self.sign,
            self.key,
            self.value
        )
        return rep


class Difference(object):
    new_keys = None
    removed_keys = None
    common_keys = None
    contents = None

    level = 0
    """Indentation level"""
    brackets = '{}'
    """Brackets symbol for rendering"""

    def __init__(self, before={}, after={}):
        self.before = before
        self.after = after

        self.find_difference(before, after)

    def find_difference(self, before, after):
        difs = []
        levelup = self.level + 1 
        childlevel = self.level + 2

        def get_diffs(status, d1, d2):
            res = []
            for k in d1.keys() - d2.keys():
                res.append(Diff(status, levelup, k, d1[k]))
            return res

        common = self.common_keys = before.keys() & after.keys()
        removed = self.removed_keys = get_diffs(STATUS['REMOVED'], before, after)
        new = self.new_keys = get_diffs(STATUS['NEW'], after, before)
        # removed = self.removed_keys = after.keys() - before.keys()

        for k in common:
            if isinstance(before[k], dict) and isinstance(after[k], dict):
                v = Difference(before[k], after[k])
                v.level = levelup
                # v.key = k
                d = Diff(STATUS['COMMON'], self.level + 1, k, v) 
                difs.append(d)
            elif before[k] == after[k]:
                difs.append(Diff(STATUS['COMMON'], childlevel, k, before[k]))
            else:
                difs.append(Diff(STATUS['REMOVED'], childlevel, k, before[k]))
                difs.append(Diff(STATUS['NEW'], childlevel, k, after[k]))

        # Add diffs to content.
        # res += mark_diff(common, level, STATUS['COMMON'])  # XXX
        # res += mark_diff(removed, levelup, STATUS['REMOVED'])
        # res += mark_diff(new, levelup, STATUS['NEW'])

        difs += new
        difs += removed

        self.contents = sorted(difs, key=lambda x: x.key)
        return self.contents

    # VISUAL
    def render(self, difs,):
        res = []
        for x in difs:
            res.append(str(x))
        res = '\n'.join(res)
        return res

    def __repr__(self):
        indent = self.level * '    '
        rep = f'''\
{self.brackets[0]}
{self.render(self.contents)}
{indent}{self.brackets[1]}'''
        return rep
