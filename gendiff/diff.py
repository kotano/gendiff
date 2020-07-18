"""Difference objects.

This module contains classes to work with differences.

TODO:
    * Remove extra levels in definitions
    * Implement nested dicts handling
"""

STATUS = {
    'COMMON': ' ',
    'NEW': '+',
    'OLD': '-',
}


def mark_diff(item, level, status=STATUS['COMMON']):
    res = []
    for k, v in item:
        res.append(
            Diff(status, level, k, v)  # NOTE
        )
    return res


class Diff(object):
    def __init__(self, status=' ', level=1, key=None, value=None):
        self.level = level
        self.sign = status
        self.key = key
        if isinstance(value, dict):
            # TODO
            self.value = Diff()
        else:
            self.value = value
        # self.value = Diff() if isinstance(value, dict) else value

    def __repr__(self):
        margin = self.level * '  '
        rep = '{}{} {} : {}'.format(
            margin,
            self.sign,
            self.key,
            self.value
        )
        return rep


class Difference(dict):
    new_items = None
    old_items = None
    common = None
    content = None

    def __init__(self, old={}, new={}):
        super().__init__()
        self.find_difference(old, new)
        self.brackets = '{}'
        """Brackets symbol for rendering"""

    def find_difference(self, dict1, dict2):
        res = []
        level = 1
        common = self.common = dict1.items() & dict2.items()
        # common = self.common = dict1.keys() & dict2.keys()
        old = self.new_items = dict1.items() - dict2.items()
        new = self.old_items = dict2.items() - dict1.items()

        res += mark_diff(common, level, STATUS['COMMON'])  # XXX
        res += mark_diff(new, level, STATUS['NEW'])
        res += mark_diff(old, level, STATUS['OLD'])
        self.content = sorted(res, key=lambda x: x.key)
        return self.content

    def render(self, difs,):
        res = []
        for x in difs:
            res.append(str(x))
        res = '\n'.join(res)
        print(res)
        return res

    def __repr__(self):
        rep = f'''\
{self.brackets[0]}
{self.render(self.content)}
{self.brackets[1]}'''
        return rep
