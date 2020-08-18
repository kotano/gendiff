"""`Diff` objects.

This module contains classes to work with differences.
"""

# STATUSES
COMMON, NEW, REMOVED, CHANGED = ' ', '+', '-', 'c'


class Change:
    """`Change` class provides info about changed attributes."""

    changedfrom = None
    """Link to previous state of diff."""

    def __init__(self, status=COMMON, key='', value=None, *, parent=''):
        """Create `Change` class instance.

        Args:

            status (str, optional): `Change`'s status sign. Defaults to ' '.
            key (str, optional): `Change` key. Defaults to ''.
            value (any, optional): `Change`'s value. Defaults to None.
            parent (object, optional): Link to parent object. Defaults to ''.
        """
        self.status = status
        self.key = key
        self.parent = parent
        self.level = parent.level + 1 if parent else 1
        self.value = self._normalize(value)

    def _normalize(self, value):
        res = value
        if isinstance(value, dict):
            res = Diff(value, value, level=self.level)
            res.parent = self
        return res

    def get_parents(self) -> list:
        """Get list of diff's parents.

        Returns:
            list(..., obj, obj): [.., grandparent, parent]."""
        # NOTE: Currently diff's parent is a `Diff` object,
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
        # Link to parent object leads to loop while serializing,
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


class Diff:
    """`Diff` class gathers information about differences
    between two dictionaries and keeps this info as `Diffs` in `contents`.

    Attributes:
        contents (list): list with `Change` objects.
        new_keys (list): list of new keys.
        common_keys (list): list of common keys.
        removed_keys (list): list of removed keys.
    """

    new_keys: list
    removed_keys: list
    common_keys: list
    contents: list

    level: int
    """Nesting level."""
    brackets: str = '{}'
    """A pair of characters to use as trailing and closing parentheses
    for rendering."""
    parent = ''
    """Parent object. Usually leads to `Change` object or empty string."""

    def __init__(self, before={}, after={}, *, level=0):
        """Create an instance of `Diff` class.

        NOTE: Executes `self.find_difference(before, after)` at the end.

        Args:

            before (dict, optional): Older dict to compare with. Defaults to {}.
            after (dict, optional): New dict. Defaults to {}.

            NOTE: For inner use.
            level (int, optional): Nesting level. Defaults to 0.

        """

        self.before = before
        self.after = after
        self.level = level

        self.common_keys = []
        self.new_keys = []
        self.removed_keys = []
        self.contents = []

        self.find_difference(before, after)

    def get_diffs(self, status, d1, d2) -> list:
        res = []
        for k in d1.keys() - d2.keys():
            res.append(Change(status, k, d1[k], parent=self))
        return res

    def find_difference(self, before: dict, after: dict):
        """Find difference between two dictionaries.

        Args:

            before (dict): Dictionary to compare with.
            after (dict): Current dictionary.

        Returns:
            list: `Diff` object's `self.contents` attribute.
        """
        difs = []

        common = self.common_keys = list(before.keys() & after.keys())
        new = self.get_diffs(NEW, after, before)
        removed = self.get_diffs(REMOVED, before, after)

        # Add diffs to content.
        difs += new
        difs += removed
        for k in common:
            if isinstance(before[k], dict) and isinstance(after[k], dict):
                v = Diff(before[k], after[k], level=self.level + 1)
                d = Change(COMMON, k, v, parent=self)
                v.parent = d
                difs.append(d)
            elif before[k] == after[k]:
                difs.append(Change(COMMON, k, before[k], parent=self))
            else:
                # Then there is changed values.
                # Show which values have changed.
                r = Change(REMOVED, k, before[k], parent=self)
                c = Change(CHANGED, k, after[k], parent=self)
                # Remember previous value
                c.changedfrom = r
                difs.append(c)

        # Update Diff attributes.
        self.new_keys = [x.key for x in new]
        self.removed_keys = [x.key for x in removed]
        self.contents = sorted(difs, key=lambda x: x.key)

        return self.contents

    # VISUAL
    def to_dict(self) -> dict:
        """Return dict representation of this object."""
        res = dict(self.__dict__)
        # Link to parent object leads to loop while serializing.
        if self.parent:
            res['parent'] = self.parent.key
        return res

    def _render_contents(self, difs):
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
{self._render_contents(self.contents)}
{indent}{self.brackets[1]}'''
        return rep
