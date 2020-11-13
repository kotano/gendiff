import pathlib

import pytest

from gendiff.diff import get_diff
from gendiff.main import load

FIXTURES = pathlib.Path(__file__).parent / 'fixtures'
SIMPLE = FIXTURES / 'simple'
NESTED = FIXTURES / 'nested'


class Simple:
    path_json = list(map(str, [SIMPLE / 'before.json', SIMPLE / 'after.json']))
    path_yml = list(map(str, [SIMPLE / 'before.yml', SIMPLE / 'after.yml']))

    res_stylish = (SIMPLE / 'res_stylish.txt').read_text()
    res_plain = (SIMPLE / 'res_plain.txt').read_text()
    res_json = load(SIMPLE / 'res_json.json')

    before = load(SIMPLE / 'before.json')
    after = load(SIMPLE / 'after.json')

    diff = get_diff(before, after)


class Nested:
    path_json = list(map(str, [NESTED / 'before.json', NESTED / 'after.json']))

    res_stylish = (NESTED / 'res_stylish.txt').read_text()
    res_plain = (NESTED / 'res_plain.txt').read_text()
    res_json = load(NESTED / 'res_json.json')

    before = load(NESTED / 'before.json')
    after = load(NESTED / 'after.json')

    diff = get_diff(before, after)


@pytest.fixture(scope='module')
def simple():
    return Simple()


@pytest.fixture(scope='module')
def nested():
    return Nested()
