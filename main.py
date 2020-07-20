"""Gendiff development main module.

Not a script!
Use this module as an entry point for development purposes and debugging.
"""

from gendiff.core import generate_diff
from gendiff.cli import get_arg_parser


def debug_simple():
    a = './tests/fixtures/simple/before.yml'
    b = './tests/fixtures/simple/after.yml'
    args = get_arg_parser().parse_args([a, b])
    res = generate_diff(args.first_file, args.second_file)
    print(res)


def debug_nested():
    a = './tests/fixtures/nested/before.json'
    b = './tests/fixtures/nested/after.json'
    args = get_arg_parser().parse_args([a, b])
    res = generate_diff(args.first_file, args.second_file)
    print(res)


if __name__ == "__main__":
    # debug_simple()
    debug_nested()
