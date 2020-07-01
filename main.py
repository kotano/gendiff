import argparse

from gendiff.scripts.core import generate_diff
# from scripts.core import generate_diff


parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', help='set format of output')


def main():
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


def debug():
    r = './tests/fixtures/simple/gendiff_result.txt'
    a = './tests/fixtures/simple/before.json'
    b = './tests/fixtures/simple/after.json'
    args = parser.parse_args([a, b])
    print(generate_diff(args.first_file, args.second_file))


if __name__ == "__main__":
    debug()
