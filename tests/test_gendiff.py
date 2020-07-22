import pytest

from gendiff.core import generate_diff
from gendiff.utils import open_file


def test_open_file():
    expected = {'host': 'hexlet.io', 'proxy': '123.234.53.22', 'timeout': 50}

    got = open_file('./tests/fixtures/simple/before.json')
    assert got == expected

    got = open_file('./tests/fixtures/simple/before.yml')
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


@pytest.mark.xfail
def test_gendiff_plain(plain_res, nested_json_path, simple_mix_path):
    expected = plain_res

    got = generate_diff(*nested_json_path, 'plain')
    assert got == expected

    got = generate_diff(*simple_mix_path, 'plain')
    assert got == expected
