import argparse

from gendiff.utils import list_package


def get_arg_parser():
    available_views = list_package('gendiff/views')
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        help='set format of output ' + str(available_views),
        default='default'
    )
    return parser
