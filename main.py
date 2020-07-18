"""Gendiff development main module.

Not a script!
Use this module as an entry point for development purposes and debugging.
"""

import argparse

from gendiff.core import generate_diff
# from core import generate_diff


parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', help='set format of output')


def main():
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


def debug():
    a = './tests/fixtures/simple/before.yml'
    b = './tests/fixtures/simple/after.yml'
    args = parser.parse_args([a, b])
    res = generate_diff(args.first_file, args.second_file)
    print(res)


if __name__ == "__main__":
    debug()
