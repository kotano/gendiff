"""Difference objects.

This module contains classes to work with differences.
"""

# STATUSES
COMMON, NEW, REMOVED, = ' ', '+', '-'


class Diff(object):
    iscomplex = False
    """Set to true if diff has a complex value."""

    def __init__(self, status=COMMON, key=None, value=None, parent=None):
        self.status = status
        self.key = key
        self.parent = parent
        self.level = parent.level + 1 if parent else 1
        self.value = self.normalize(value)

    def normalize(self, value):
        res = value
        if isinstance(value, dict):
            res = Difference(value, value, self.level, self)
            res.iscomplex = True
        return res

    # def to_plain(self):
    #     template = "Property '{}' was {}"
    #     if self.status == NEW:
    #         pass
    #     elif self.status == REMOVED:
    #         return

    def __str__(self):
        indent = self.level * 2 * ' '
        rep = '{}{} {}: {}'.format(
            indent,
            self.status,
            self.key,
            self.value
        )
        return rep


class Difference(object):
    new_keys = None
    removed_keys = None
    common_keys = None
    contents = []

    level: int
    """Indentation level."""
    brackets = '{}'
    """Pair of symbols to use as ending and closing brackets for rendering."""

    def __init__(self, before={}, after={}, level=0, parent=None):
        self.before = before
        self.after = after
        self.level = level
        self.parent = parent

        self.find_difference(before, after)

    def find_difference(self, before, after):
        difs = []

        def get_diffs(status, d1, d2):
            res = []
            for k in d1.keys() - d2.keys():
                res.append(Diff(status, k, d1[k], self))
            return res

        common = self.common_keys = before.keys() & after.keys()
        new = self.new_keys = get_diffs(NEW, after, before)
        removed = self.removed_keys = get_diffs(REMOVED, before, after)

        for k in common:
            if isinstance(before[k], dict) and isinstance(after[k], dict):
                v = Difference(before[k], after[k], self.level + 1)
                d = Diff(COMMON, k, v, self)
                v.parent = d
                difs.append(d)
            elif before[k] == after[k]:
                difs.append(Diff(COMMON, k, before[k], self))
            # Then there is changed values.
            else:
                # Show which values have changed.
                difs.append(Diff(REMOVED, k, before[k], self))
                difs.append(Diff(NEW, k, after[k], self))

        # Add diffs to content.
        difs += new
        difs += removed

        self.contents = sorted(difs, key=lambda x: x.key)
        return self.contents

    # VISUAL
    def render(self, difs):
        res = []
        for x in difs:
            res.append(str(x))
        res = '\n'.join(res)
        return res

    # def plain_view(self):
    #     res = []
    #     for x in self.contents:
    #         pass

    def __str__(self):
        ind = self.level + 1 if self.parent else self.level
        indent = ind * 2 * ' '
        rep = f'''\
{self.brackets[0]}
{self.render(self.contents)}
{indent}{self.brackets[1]}'''
        return rep
