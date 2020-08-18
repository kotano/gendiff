from gendiff.views import plain, json as jason, default
import json

import pytest


def test_default_view(
        simple_difference, simple_res,
        nested_difference, nested_res):
    expected = simple_res
    got = default.render(simple_difference)
    assert got == expected, 'simple failed'

    expected = nested_res
    got = default.render(nested_difference)
    assert got == expected, 'nested failed'


def test_plain_view(
        nested_plain_view_res, simple_plain_view_res,
        simple_difference, nested_difference):

    expected = simple_plain_view_res
    got = plain.render(simple_difference)
    assert got == expected

    expected = nested_plain_view_res
    got = plain.render(nested_difference)
    assert got == expected
    pass


@pytest.mark.xfail
def test_json_view(
        simple_difference, nested_difference,
        simple_json_view_dict, nested_json_view_dict):

    got = json.loads(jason.render(simple_difference))
    expected = simple_json_view_dict
    assert got == expected, 'simple failed'

    got = json.loads(jason(nested_difference))
    expected = nested_json_view_dict
    assert got == expected, 'nested failed'
