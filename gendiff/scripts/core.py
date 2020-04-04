import json
from builtins import isinstance

import yaml

# TODO Refactor. Too many variables
# TODO Bring file management to separate module


def open_file(path):
    '''Takes .json or .yml file as arg and returns
    dictionary with their contents.'''
    with open(path) as f:
        data = yaml.safe_load(f) if path.split(
            '.')[-1] == 'yml'else json.load(f)
    return (data)


def convert_to_tuple(d: dict):
    res = {}
    for k, v in d.items():
        if isinstance(v, dict):
            res[k] = convert_to_tuple(v)
        else:
            res[k] = v
    return tuple(res.items())


def compare_values(val1, val2):
    before = set(convert_to_tuple(val1))
    after = set(convert_to_tuple(val2))
    
    common = before & after
    new = after - before
    old = before - after

    xcommon = {(' ',) + x for x in common}
    xnew = {('+',) + x for x in new}
    xold = {('-',) + x for x in old}

    mix = sorted(list(xcommon | xnew | xold), key=lambda x: (x[1], x[2]))
    for x in mix:
        print(x)
    res = format(mix)
    return res


def generate_diff(file1, file2):
    '''Returns json-like string representing difference between two files'''
    # TODO fix relative paths
    data1 = open_file(file1)
    data2 = open_file(file2)

    def mark(data1, data2):
        mix = data1.keys() & data2.keys()
        for x in mix:
            if isinstance(data1[x], dict) and isinstance(data2[x], dict):
                compare_values(data1[x], data2[x])
            # if isins data1[mix]
            # dif = data1[x].values() & data2[x].values()

        before = set(convert_to_tuple(data1))
        after = set(convert_to_tuple(data2))

        common = before & after
        new = after - before
        old = before - after

        xcommon = {(' ',) + x for x in common}
        xnew = {('+',) + x for x in new}
        xold = {('-',) + x for x in old}

        mix = sorted(list(xcommon | xnew | xold), key=lambda x: (x[1], x[2]))
        res = []
        # for x in mix:
        #     if isinstance(x[-1], tuple):

    def diff(data1, data2):
        res = {}
        comm = data1.keys() & data2.keys()
        for x in comm:
            if isinstance(data1[x], dict) and isinstance(data2[x], dict):
                res[x] = (diff(data1[x], data2[x]))

        before = set(convert_to_tuple(data1))
        after = set(convert_to_tuple(data2))

        common = before & after
        new = after - before
        old = before - after

        xcommon = {(' ',) + x for x in common}
        xnew = {('+',) + x for x in new}
        xold = {('-',) + x for x in old}

        mix = sorted(list(xcommon | xnew | xold), key=lambda x: (x[1], x[2]))
        for x in mix:
            print(x)
            print(res)
        return mix
        # res = format(mix)
        # return res

    return diff(data1, data2)


def format(lst):
    for elem in lst:
        if isinstance(elem[-1], tuple):
            return format(elem[-1])

        elif isinstance(lst, tuple):
            print('format', lst)
            value = '\n'.join(
                ['  {} {} : {{\n{}\n    }}'.format(*elems) for elems in lst])

        else:
            value = '\n'.join(['  {} {} : {}'.format(*elems) for elems in lst])

    output = '''{{\n{}\n}}'''.format(value)
    return output


def test_gendiff_nested():
    f = open('./tests/fixtures/gendiff_nested_res.txt')
    # right_answer = f.read()

    answer = (generate_diff(
        './tests/fixtures/before.json',
        './tests/fixtures/after.json'))
    # print(answer == right_answer)
    print(answer)


def test_gendiff_json():
    f = open('./tests/fixtures/simple/gendiff_result.txt')
    # right_answer = f.read()

    answer = (generate_diff(
        './tests/fixtures/simple/before.json',
        './tests/fixtures/simple/after.json'))
    # print(answer == right_answer)
    print(answer)


# test_gendiff_json()
test_gendiff_nested()
