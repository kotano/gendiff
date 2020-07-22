import pytest

from gendiff.diff import Difference
from gendiff.utils import open_file


def safe_read(filepath):
    with open(filepath) as f:
        return f.read()


@pytest.fixture
def simple_json_path():
    return ('./tests/fixtures/simple/before.json',
            './tests/fixtures/simple/after.json')


@pytest.fixture
def simple_yml_path():
    return ('./tests/fixtures/simple/before.yml',
            './tests/fixtures/simple/after.yml')


@pytest.fixture
def simple_mix_path():
    return ('./tests/fixtures/simple/before.yml',
            './tests/fixtures/simple/after.json')


@pytest.fixture
def simple_res():
    return safe_read('./tests/fixtures/simple/gendiff_res.txt')


@pytest.fixture
def nested_json_path():
    return ('./tests/fixtures/nested/before.json',
            './tests/fixtures/nested/after.json')


@pytest.fixture
def nested_res():
    return safe_read('./tests/fixtures/nested/gendiff_nested_res.txt')


@pytest.fixture
def plain_res():
    return safe_read('./tests/fixtures/plain_res.txt')


@pytest.fixture
def changed_dicts_simple(simple_json_path):
    file1 = open_file(simple_json_path[0])
    file2 = open_file(simple_json_path[1])
    return file1, file2


@pytest.fixture
def changed_dicts_nested(nested_json_path):
    file1 = open_file(nested_json_path[0])
    file2 = open_file(nested_json_path[1])
    return file1, file2


@pytest.fixture
def simple_difference(changed_dicts_simple):
    return Difference(*changed_dicts_simple)


@pytest.fixture
def nested_difference(changed_dicts_nested):
    return Difference(*changed_dicts_nested)
