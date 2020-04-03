import json
import os


# TODO Refactor. Too many variables

def open_files(path1, path2):
    with open(path1) as f1:
        data1 = json.load(f1)
        with open(path2) as f2:
            data2 = json.load(f2)
    return (data1, data2)


def generate_diff(file1, file2):
    try:
        # print(file1, file2)
        data1, data2 = open_files(file1, file2)
    except FileNotFoundError:
        # WRONG
        print('Searching for relative paths')
        DIRNAME = os.path.dirname(__file__)
        path1 = os.path.join(DIRNAME, file1)
        path2 = os.path.join(DIRNAME, file2)

        data1, data2 = open_files(path1, path2)

    before = set(data1.items())
    after = set(data2.items())

    common = before & after
    new = after - before
    old = before - after

    xcommon = {(' ',) + x for x in common}
    xnew = {('+',) + x for x in new}
    xold = {('-',) + x for x in old}

    # TODO check sort behavior
    mix = sorted(list(xcommon | xnew | xold), key=lambda x: (x[1], x[2]))

    result = '\n'.join(['  {} {} : {}'.format(*elems) for elems in mix])

    result = '''{{\n{}\n}}'''.format(result)
    return result
