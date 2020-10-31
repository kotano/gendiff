from gendiff.cli import get_arg_parser
from gendiff.main import generate_diff, load


def test_safe_load():
    expected = {'host': 'hexlet.io', 'proxy': '123.234.53.22', 'timeout': 50}

    got = load('./tests/fixtures/simple/before.json')
    assert got == expected

    got = load('./tests/fixtures/simple/before.yml')
    assert got == expected


def test_cli_get_argparser(simple):
    args = get_arg_parser().parse_args([*simple.path_json])

    expected = simple.res_default
    got = generate_diff(args.first_file, args.second_file)
    assert got == expected


def test_gendiff(simple):
    expected = simple.res_default
    got = generate_diff(*simple.path_json)
    assert got == expected

    got = generate_diff(*simple.path_yml)
    assert got == expected


def test_gendiff_nested(nested):
    expected = nested.res_default
    got = generate_diff(*nested.path_json)
    assert got == expected


def test_gendiff_plain(simple, nested):
    expected = simple.res_plain
    got = generate_diff(*simple.path_json, 'plain')
    assert got == expected

    expected = nested.res_plain
    got = generate_diff(*nested.path_json, 'plain')
    assert got == expected
