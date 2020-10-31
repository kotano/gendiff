from collections import OrderedDict


CHANGED, UNCHANGED, ADDED, DELETED, NESTED = 'C', 'U', 'A', 'D', 'N'


def find_difference(status, d1, d2) -> dict:
    res = {}
    for key in d1.keys() - d2.keys():
        res[key] = (status, d1[key])
    return res


def get_diff(before: dict, after: dict) -> dict:
    """Find difference between two dictionaries.

    Args:

        before (dict): Dictionary to compare with.
        after (dict): Current dictionary.

    Returns:
        dict: Dictionary in `key: [status, value, *new_value]` format.
    """
    diff = {}
    # Add new keys
    diff.update(find_difference(ADDED, after, before))
    # Add removed keys
    diff.update(find_difference(DELETED, before, after))
    # Handle common keys
    for key in before.keys() & after.keys():
        before_val = before[key]
        after_val = after[key]
        if isinstance(before[key], dict) and isinstance(after[key], dict):
            # If both values are dictionaries, then find their differences.
            diff[key] = (NESTED, get_diff(before_val, after_val))
        elif before[key] == after[key]:
            # If values are same
            diff[key] = (UNCHANGED, before_val)
        else:
            # Else there is changed values.
            # Show which values have changed.
            diff[key] = (CHANGED, before_val, after_val)

    return OrderedDict(sorted(diff.items(), key=lambda kv: kv[0]))
