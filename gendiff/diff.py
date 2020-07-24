"""Difference objects.

This module contains classes to work with differences.
"""

# STATUSES
COMMON, NEW, REMOVED, CHANGED = ' ', '+', '-', 'c'


class DiffBase(object):
    # NOTE: Future
    # FIXME: Tests don't pass when DiffBase inherits from dict

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

        # pass


class Diff(DiffBase):
    changedfrom = None
    """Link to previous state of diff."""

    def __init__(self, status=COMMON, key=None, value=None, parent=''):
        self.status = status
        self.key = key
        self.parent = parent
        self.level = parent.level + 1 if parent else 1
        self.value = self.normalize(value)

    def normalize(self, value):
        res = value
        if isinstance(value, dict):
            res = Difference(value, value, self.level, self)
        return res

    def get_parents(self) -> list:
        """Get list of diff's parents.

        Returns:
            list(..., obj, obj): [.., grandparent, parent]."""
        # NOTE: Currently diff's parent is a difference object,
        # so we have to call parent twice to get previous diff.
        res = []
        if self.parent:
            previous_diff = self.parent.parent
            if previous_diff and previous_diff.parent:
                res += previous_diff.get_parents()
            if previous_diff:
                res.append(previous_diff)
        return res

    def to_dict(self):
        res = dict(self.__dict__)
        # Link to parent object leads to loop while deserializing,
        # so it is better to simply leave parent's key in the list.
        res['parent'] = [x.key for x in self.get_parents()]
        return res

    # VISUAL
    def __str__(self):
        template = '{}{} {}: {}'
        indent = self.level * 2 * ' '
        status = self.status

        if self.status == CHANGED:
            # Add previous diff on top of current
            template = '{}\n{}'.format(str(self.changedfrom), template)
            status = NEW

        res = template.format(
            indent,
            status,
            self.key,
            self.value
        )

        return res


class Difference(DiffBase):
    new_keys = []
    removed_keys = []
    common_keys = []
    contents = []

    level: int
    """Nesting level."""
    brackets = '{}'
    """Pair of symbols to use as ending and closing brackets for rendering."""

    def __init__(self, before={}, after={}, level=0, parent=''):
        self.before = before
        self.after = after
        self.level = level
        self.parent = parent

        self.find_difference(before, after)

    def get_diffs(self, status, d1, d2):
        res = []
        for k in d1.keys() - d2.keys():
            res.append(Diff(status, k, d1[k], self))
        return res

    def find_difference(self, before, after):
        difs = []

        common = self.common_keys = list(before.keys() & after.keys())
        new = self.get_diffs(NEW, after, before)
        removed = self.get_diffs(REMOVED, before, after)

        # Add diffs to content.
        difs += new
        difs += removed
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
                r = Diff(REMOVED, k, before[k], self)
                c = Diff(CHANGED, k, after[k], self)
                # Remember previous value
                c.changedfrom = r
                difs.append(c)

        # Update difference attributes.
        self.new_keys = [x.key for x in new]
        self.removed_keys = [x.key for x in removed]
        self.contents = sorted(difs, key=lambda x: x.key)

        return self.contents

    # VISUAL
    def to_dict(self):
        res = dict(self.__dict__)

        # Link to parent object leads to loop while deserializing.
        if self.parent:
            res['parent'] = self.parent.key

        # Remove redundant links in dict.
        # res['new_keys'] = [x.key for x in self.removed_keys]
        # res['removed_keys'] = [x.key for x in self.removed_keys]

        return res

    def render(self, difs):
        res = []
        for x in difs:
            res.append(str(x))
        res = '\n'.join(res)
        return res

    def __str__(self):
        # Indentation for closing bracket.
        inc = self.level + 1 if self.parent else self.level
        indent = inc * 2 * ' '
        rep = f'''\
{self.brackets[0]}
{self.render(self.contents)}
{indent}{self.brackets[1]}'''
        return rep
