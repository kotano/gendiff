import json


# TODO Refactor. Too many variables

def generate_diff(file1, file2):
    try:
        with open(file1) as f1:
            data1 = json.load(f1)
            with open(file2) as f2:
                data2 = json.load(f2)
    except FileNotFoundError:
        print('File does not exist')
        return

    before = set(data1.items())
    after = set(data2.items())

    common = before & after
    new = after - before
    old = before - after

    xcommon = {(' ',) + x for x in common}
    xnew = {('+',) + x for x in new}
    xold = {('-',) + x for x in old}

    mix = list(xcommon | xnew | xold)

    # TODO not stable sort
    result = '\n'.join(['  {} {} : {}'.format(*elems) for elems in sorted(
        mix, key=lambda x: (x[1], x[2]))])

    result = '''{{\n{} \n}}'''.format(result)
    return result
