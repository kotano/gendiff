import argparse

from gendiff.views import VIEWS

available_views = list(VIEWS.keys())


def get_arg_parser() -> object:
    """Make argument parser.

    Returns:
        object: Argument parser object.
    """
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        help='set format of output ' + repr(available_views),
        default='stylish', type=str
    )
    return parser


def parse_args() -> object:
    """Handle user arguments and return.

    Returns:
        object: User arguments
    """
    args = get_arg_parser().parse_args()
    if args.format not in available_views:
        print("Unsupported format.")
        exit()
    return args
