import json
import os
from builtins import isinstance

import yaml

# TODO Refactor. Too many variables
# TODO Bring file management to separate module


def open_files(path1, path2):
    '''Takes two .json or .yml files as args and returns
    dictionaries with their contents.'''
    with open(path1) as f1:
        with open(path2) as f2:
            data1 = yaml.safe_load(f1) if path1.split(
                '.')[-1] == 'yml'else json.load(f1)
            data2 = yaml.safe_load(f2) if path2.split(
                '.')[-1] == 'yml' else json.load(f2)
    return (data1, data2)


# TODO fix relative paths
def generate_diff(file1, file2):
    '''Returns json-like string representing difference between two files'''
    try:
        data1, data2 = open_files(file1, file2)
    except FileNotFoundError:
        # WRONG
        print('Searching for relative paths')
        DIRNAME = os.path.dirname(__file__)
        path1 = os.path.join(DIRNAME, file1)
        path2 = os.path.join(DIRNAME, file2)

        data1, data2 = open_files(path1, path2)

    def convert_to_tuple(d: dict):
        res = {}
        for k, v in d.items():
            if isinstance(v, dict):
                res[k] = convert_to_tuple(v)
            else:
                res[k] = v

        return tuple(res.items())

    def to_tuple(d):
        result = []
        for k, v in d.items():
            if isinstance(v, dict):
                result.append([k])
                k.extend(to_tuple(v))
            else:
                result.append((k, v))
        return result

    def diff(data1, data2):
        before = set(convert_to_tuple(data1))
        after = set(convert_to_tuple(data2))

        common = before & after
        new = after - before
        old = before - after

        xcommon = {(' ',) + x for x in common}
        xnew = {('+',) + x for x in new}
        xold = {('-',) + x for x in old}

        mix = sorted(list(xcommon | xnew | xold), key=lambda x: (x[1], x[2]))
        res = format(mix)
        return res

    return diff(data1, data2)


def format(lst):
    result = '\n'.join(['  {} {} : {}'.format(*elems) for elems in lst])

    result = '''{{\n{}\n}}'''.format(result)
    return result


def test_gendiff_nested():
    f = open('./tests/fixtures/gendiff_nested_res.txt')
    right_answer = f.read()

    answer = (generate_diff(
        './tests/fixtures/before.json',
        './tests/fixtures/after.json'))
    assert(answer == right_answer)


test_gendiff_nested()
