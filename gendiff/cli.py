import argparse

from gendiff.views import VIEWS

available_views = list(VIEWS.keys())


def get_arg_parser():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        help='set format of output ' + repr(available_views),
        default='default', type=str
    )
    argparse.ArgumentParser()
    return parser
