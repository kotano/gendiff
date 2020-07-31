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
    """Diff class provides info about changed attributes."""

    changedfrom = None
    """Link to previous state of diff."""

    def __init__(self, status=COMMON, key='', value=None, *, parent=''):
        """Create Diff class instance.

        Args:

            status (str, optional): Diff's status sign. Defaults to ' '.
            key (str, optional): Diff key. Defaults to ''.
            value (any, optional): Diff's value. Defaults to None.
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
            res = Difference(value, value, level=self.level)
            res.parent = self
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


class Difference(DiffBase):
    """Difference class gathers information about differences
    between two dictionaries.

    Attributes:
        contents (list): list with `Diff` objects.
        new_keys (list): list of new keys.
        common_keys (list): list of common keys.
        removed_keys (list): list of removed keys.

    Methods:
        find_difference -> list
        get_diffs -> list
        to_dict -> dict
    """

    new_keys = []
    removed_keys = []
    common_keys = []
    contents = []

    level: int
    """Nesting level."""
    brackets = '{}'
    """A pair of characters to use as trailing and closing parentheses
    for rendering."""
    parent = ''
    """Parrent object. Usually leads to Diff object or empty string."""

    def __init__(self, before={}, after={}, *, level=0):
        """Create an instance of Difference class.

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

        self.find_difference(before, after)

    def get_diffs(self, status, d1, d2) -> list:
        res = []
        for k in d1.keys() - d2.keys():
            res.append(Diff(status, k, d1[k], parent=self))
        return res

    def find_difference(self, before: dict, after: dict):
        """Find difference between two dictionaries.

        Args:

            before (dict): Dictionary to compare with.
            after (dict): Current dictionary.

        Returns:
            list: Difference object's `self.contents` attribute.
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
                v = Difference(before[k], after[k], level=self.level + 1)
                d = Diff(COMMON, k, v, parent=self)
                v.parent = d
                difs.append(d)
            elif before[k] == after[k]:
                difs.append(Diff(COMMON, k, before[k], parent=self))
            else:
                # Then there is changed values.
                # Show which values have changed.
                r = Diff(REMOVED, k, before[k], parent=self)
                c = Diff(CHANGED, k, after[k], parent=self)
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
        """Return dict representation of this object.

        Returns: Object's __dict__
        """
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
