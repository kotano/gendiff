import pytest

from gendiff.core import generate_diff


def test_gendiff_json():
    f = open('./tests/fixtures/simple/gendiff_result.txt')
    right_answer = f.read()

    answer = generate_diff(
        './tests/fixtures/simple/before.json',
        './tests/fixtures/simple/after.json')
    assert answer == right_answer


def test_gendiff_yml():
    f = open('./tests/fixtures/simple/gendiff_result.txt')
    right_answer = f.read()

    answer = generate_diff(
        './tests/fixtures/simple/before.yml',
        './tests/fixtures/simple/after.yml')
    assert answer == right_answer


@pytest.mark.xfail
def test_gendiff_nested():
    f = open('./tests/fixtures/nested/gendiff_nested_res.txt')
    right_answer = f.read()

    answer = generate_diff(
        './tests/fixtures/nested/before.json',
        './tests/fixtures/nested/after.json')
    assert answer == right_answer
