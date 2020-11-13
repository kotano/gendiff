import pathlib
import json

import pytest

from gendiff.main import generate_diff

FIXTURES = pathlib.Path(__file__).parent / 'fixtures'
SIMPLE = FIXTURES / 'simple'
NESTED = FIXTURES / 'nested'


@pytest.mark.parametrize('path', [SIMPLE, NESTED])
def test_gendiff_stylish(path):
    with open(path / 'res_stylish.txt') as f:
        expected = f.read()
    got = generate_diff(path / 'before.json', path / 'after.json', 'stylish')
    assert got == expected


@pytest.mark.parametrize('path', [SIMPLE, NESTED])
def test_gendiff_plain(path):
    with open(path / 'res_plain.txt') as f:
        expected = f.read()
    got = generate_diff(path / 'before.json', path / 'after.json', 'plain')
    assert got == expected


@pytest.mark.parametrize('path', [SIMPLE, NESTED])
def test_gendiff_json(path):
    with open(path / 'res_json.json') as f:
        expected = json.load(f)
    got = json.loads(generate_diff(
        path / 'before.json', path / 'after.json', 'json'))
    assert got == expected
