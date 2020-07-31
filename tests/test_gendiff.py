from gendiff.cli import get_arg_parser
from gendiff.core import generate_diff
from gendiff.utils import safe_load


def test_safe_load():
    expected = {'host': 'hexlet.io', 'proxy': '123.234.53.22', 'timeout': 50}

    got = safe_load('./tests/fixtures/simple/before.json')
    assert got == expected

    got = safe_load('./tests/fixtures/simple/before.yml')
    assert got == expected


def test_cli_get_argparser(simple_res, simple_json_path):
    args = get_arg_parser().parse_args([*simple_json_path])

    expected = simple_res
    got = generate_diff(args.first_file, args.second_file)
    assert got == expected


def test_gendiff_json(simple_json_path, simple_res):
    expected = simple_res
    got = generate_diff(*simple_json_path)
    assert got == expected


def test_gendiff_yml(simple_yml_path, simple_res):
    expected = simple_res
    got = generate_diff(*simple_yml_path)
    assert got == expected


def test_gendiff_nested(nested_json_path, nested_res):
    expected = nested_res
    got = generate_diff(*nested_json_path)
    assert got == expected


def test_gendiff_plain(
        nested_plain_view_res, simple_plain_view_res,
        nested_json_path, simple_mix_path):
    expected = nested_plain_view_res
    got = generate_diff(*nested_json_path, 'plain')
    assert got == expected

    expected = simple_plain_view_res
    got = generate_diff(*simple_mix_path, 'plain')
    assert got == expected
