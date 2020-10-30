"""Default view returns json-like string of diff contents.

EXAMPLE
>>> generate_diff(before, after, 'default')
{
    common: {
        setting1: Value 1
      - setting2: 200
        setting3: True
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
      - setting6: {
            key: value
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
    }
  - group2: {
        abc: 12345
    }
  + group3: {
        fee: 100500
    }
}
"""

from gendiff import diff

status_maps = {
    diff.UNCHANGED: "{ind}  {key}: {val}\n",
    diff.ADDED: "{ind}+ {key}: {val}\n",
    diff.DELETED: "{ind}- {key}: {val}\n",
    # diff.NESTED: "{ind}  {key}: {{\n{contents}}}\n",
    diff.NESTED: "{ind}  {key}: {{\n",
    diff.CHANGED: "{ind}- {key}: {before}\n{ind}+ {key}: {after}\n"
}

first_line = "{ind}{sign} {key}: {{\n"


def render_value(val, indent):
    if isinstance(val, dict):
        ind = '  ' * indent
        temp = []
        for ke, va in val.items():
            temp.append("{ind}  {key}: {val}\n".format(
                ind=ind, key=ke, val=va))
        conts = ''.join(temp)
        res = "{{\n{conts}{ind}}}".format(conts=conts, ind=ind * 2)
        return res
    else:
        return val


def default_view(dif, depth=1):
    res = []
    ind = '  ' * depth
    for k, v in dif.items():
        status, *values = v
        if status == diff.NESTED:
            # "{ind}  {key}: {{\n".format(ind=ind, key=k)
            # first_line = status_maps[status].format(ind=ind, key=k)
            # contents = default_view(values[0], indent + 2)
            # last_line = '  ' * (indent * 2) + "}\n"
            # res.append(status_maps[status].format())
            res.append(status_maps[status].format(ind=ind, key=k))
            res += default_view(values[0], depth + 2)
            res.append(ind * 2 + "}\n")
        elif status == diff.CHANGED:
            res.append(status_maps[status].format(
                ind=ind, key=k,
                before=values[0], after=values[1]))
        else:
            # val = render_value(values[0], depth + 2)
            val = values[0]
            if isinstance(val, dict):
                temp = []
                for ke, va in val.items():
                    temp.append("{ind}  {key}: {val}\n".format(
                        ind=ind, key=ke, val=va))
                conts = ''.join(temp)
                val = "{{\n{conts}{ind}}}".format(conts=conts, ind=ind * 2)
                # val = "{{\n"
                # res.append(first_line.format(ind=ind, sign=))
                # val = "{{ }}"
            res.append(status_maps[status].format(
                ind=ind, key=k, val=val))
    return res


def render(diff):
    contents = ''.join(default_view(diff))
    string = "{{\n{contents}\n}}".format(contents=contents)
    return string


# def render(dif) -> str:
#     return 'NO'
#     return draw_diff(dif)


# #

# def draw_diff(dif) -> str:
#     # Indentation for closing bracket.
#     depth = dif.level + 1 if dif.parent else dif.level
#     indent = depth * 2 * ' '
#     contents = '\n'.join([draw_change(x) for x in dif.contents])
#     template = (
#         "{{\n"
#         "{contents}\n"
#         "{indent}""}}"
#     )
#     res = template.format(
#         contents=contents,
#         indent=indent
#     )
#     return res


# def draw_change(change) -> str:
#     template = '{}{} {}: {}'
#     indent = change.level * 2 * ' '
#     status = change.status
#     value = change.value
#     if isinstance(value, diff.Diff):
#         value = draw_diff(change.value)

#     if change.status == diff.MODIFIED:
#         # Add previous diff on top of current
#         template = '{}\n{}'.format(draw_change(change.changedfrom), template)
#         status = diff.NEW

#     res = template.format(
#         indent,
#         sign_maps[status],  # Change status text to symbol.
#         change.key,
#         value
#     )
#     return res
