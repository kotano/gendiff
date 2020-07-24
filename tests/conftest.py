import pytest

from gendiff.diff import Difference
from gendiff.utils import safe_load, safe_read


# RESULTS
@pytest.fixture
def simple_res():
    return safe_read('./tests/fixtures/simple/gendiff_res.txt')


@pytest.fixture
def nested_res():
    return safe_read('./tests/fixtures/nested/gendiff_nested_res.txt')


@pytest.fixture
def simple_plain_view_res():
    return safe_read('./tests/fixtures/simple/plain_res.txt')


@pytest.fixture
def nested_plain_view_res():
    return safe_read('./tests/fixtures/nested/plain_res.txt')
#


# PATHS
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
def nested_json_path():
    return ('./tests/fixtures/nested/before.json',
            './tests/fixtures/nested/after.json')


@pytest.fixture
def simple_difference(changed_dicts_simple):
    return Difference(*changed_dicts_simple)


@pytest.fixture
def nested_difference(changed_dicts_nested):
    return Difference(*changed_dicts_nested)
#


# DICTIONARIES
@pytest.fixture
def changed_dicts_simple(simple_json_path):
    """ `before.json` and `afer.json` deserialized contents."""
    file1 = safe_load(simple_json_path[0])
    file2 = safe_load(simple_json_path[1])
    return file1, file2


@pytest.fixture
def changed_dicts_nested(nested_json_path):
    """ `before.json` and `afer.json` deserialized contents."""
    file1 = safe_load(nested_json_path[0])
    file2 = safe_load(nested_json_path[1])
    return file1, file2


@pytest.fixture
def simple_json_view_dict():
    return safe_load('./tests/fixtures/simple/json_view_res.json')


@pytest.fixture
def nested_json_view_dict():
    return safe_load('./tests/fixtures/nested/json_view_res.json')
#
