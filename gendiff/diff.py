"""`Diff` objects.

This module contains classes to work with differences.
"""
from copy import deepcopy

# STATUSES
COMMON, NEW, REMOVED, MODIFIED = 'C', 'N', 'R', 'M'


class Change:
    """`Change` class provides info about `Diff`'s changed attributes."""

    def __init__(self, status, key='', value=None, *, parent=''):
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

        self.changedfrom = None
        """Link to previous state of diff."""

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

    def serialize(self):
        return {'status': self.status, 'value': self.value}


class Diff:
    """`Diff` class gathers information about differences
    between two dictionaries and keeps this info as `Changes` in `contents`.

    Attributes:
        contents (list): list with `Change` objects.
    """

    contents: list
    level: int
    """Nesting level."""

    def __init__(self, before: dict, after: dict, *, level=0):
        """Create an instance of `Diff` class.

        NOTE: Executes `self.find_difference(before, after)` at the end.

        Args:

            before (dict): Older dict to compare with. Defaults to {}.
            after (dict): New dict. Defaults to {}.

            NOTE: For inner use.
            level (int, optional): Nesting level. Defaults to 0.

        """

        self.before = deepcopy(before)
        self.after = deepcopy(after)
        self.level = level
        self.contents = []
        self.parent = ''

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

        common = sorted(before.keys() & after.keys())
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
                c = Change(MODIFIED, k, after[k], parent=self)
                # Remember previous value.
                c.changedfrom = r
                difs.append(c)

        # Update Diff attributes.
        self.contents = sorted(difs, key=lambda x: x.key)
        return self.contents

    # VISUAL
    def serialize(self) -> dict:
        """Return deserializable representation of this object."""
        res = {}
        for c in self.contents:
            res[c.key] = c
        return res
