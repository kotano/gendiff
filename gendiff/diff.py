from collections import OrderedDict


CHANGED, UNCHANGED, ADDED, DELETED, NESTED = 'C', 'U', 'A', 'D', 'N'


def find_difference(before: dict, after: dict):
    """Find difference between two dictionaries.

    Args:

        before (dict): Dictionary to compare with.
        after (dict): Current dictionary.

    Returns:
        list: `Diff` object's `self.contents` attribute.
    """
    # STRUCTURE: `key: (status, value)`
    diff = {}
    before_keys = before.keys()
    after_keys = after.keys()

    # Add new keys
    for key in after_keys - before_keys:
        diff[key] = (ADDED, after[key])
    # Add removed keys
    for key in before_keys - after_keys:
        diff[key] = (DELETED, before[key])

    # Handle common keys
    for key in before_keys & after_keys:
        before_val = before[key]
        after_val = after[key]
        if isinstance(before[key], dict) and isinstance(after[key], dict):
            # If both values are dictionaries, then find their differences.
            diff[key] = (NESTED, find_difference(before_val, after_val))
        elif before[key] == after[key]:
            # If values are same
            diff[key] = (UNCHANGED, before_val)
        else:
            # Else there is changed values.
            # Show which values have changed.
            diff[key] = (CHANGED, before_val, after_val)

    return OrderedDict(sorted(diff.items(), key=lambda kv: kv[0]))
