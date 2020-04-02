import argparse
import json

# TODO Refactor. Too many variables

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', help='set format of output')


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

    mix = xcommon | xnew | xold

    # TODO not stable sort
    result = '\n'.join(['  {} {} : {}'.format(*elems) for elems in sorted(
        mix, key=lambda x: x[1])])

    result = '''{{\n{} \n}}'''.format(result)
    print(result)
    return result


def main():
    args = parser.parse_args()
    generate_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    main()
