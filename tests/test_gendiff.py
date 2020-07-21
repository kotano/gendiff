import pytest

from gendiff.core import generate_diff
from gendiff.utils import open_file


def test_open_file():
    got = open_file('./tests/fixtures/simple/before.json')
    expected = {'host': 'hexlet.io', 'proxy': '123.234.53.22', 'timeout': 50}
    assert got == expected

    got = open_file('./tests/fixtures/simple/before.yml')
    assert got == expected


def test_gendiff_json():
    expected = open('./tests/fixtures/simple/gendiff_result.txt').read()
    got = generate_diff(
        './tests/fixtures/simple/before.json',
        './tests/fixtures/simple/after.json')
    assert got == expected


def test_gendiff_yml():
    expected = open('./tests/fixtures/simple/gendiff_result.txt').read()
    got = generate_diff(
        './tests/fixtures/simple/before.yml',
        './tests/fixtures/simple/after.yml')
    assert got == expected


def test_gendiff_nested():
    expected = open('./tests/fixtures/nested/gendiff_nested_res.txt').read()
    got = generate_diff(
        './tests/fixtures/nested/before.json',
        './tests/fixtures/nested/after.json')
    assert got == expected


@pytest.mark.xfail
def test_gendiff_plain():
    expected = open('./tests/fixtures/plain_res.txt').read()
    got = generate_diff(
        './tests/fixtures/nested/before.json',
        './tests/fixtures/nested/after.json')
    assert got == expected
