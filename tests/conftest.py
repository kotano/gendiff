import pathlib

import pytest

from gendiff.diff import Diff
from gendiff.core import load

FIXTURES = pathlib.Path(__file__).parent / 'fixtures'
SIMPLE = FIXTURES / 'simple'
NESTED = FIXTURES / 'nested'


class Simple:
    path_json = list(map(str, [SIMPLE / 'before.json', SIMPLE / 'after.json']))
    path_yml = list(map(str, [SIMPLE / 'before.yml', SIMPLE / 'after.yml']))

    res_default = (SIMPLE / 'res_default.txt').read_text()
    res_plain = (SIMPLE / 'res_plain.txt').read_text()
    res_json = load(SIMPLE / 'res_json.json')

    before = load(SIMPLE / 'before.json')
    after = load(SIMPLE / 'after.json')

    diff = Diff(before, after)


class Nested:
    path_json = list(map(str, [NESTED / 'before.json', NESTED / 'after.json']))

    res_default = (NESTED / 'res_default.txt').read_text()
    res_plain = (NESTED / 'res_plain.txt').read_text()
    res_json = load(NESTED / 'res_json.json')

    before = load(NESTED / 'before.json')
    after = load(NESTED / 'after.json')

    diff = Diff(before, after)


@pytest.fixture(scope='module')
def simple():
    return Simple()


@pytest.fixture(scope='module')
def nested():
    return Nested()
