import json

from gendiff.views import plain, json as jason, stylish


def test_stylish_view_simple(simple):
    expected = simple.res_stylish
    got = stylish.render(simple.diff)
    assert got == expected, 'simple failed'


def test_stylish_view_nested(nested):
    expected = nested.res_stylish
    got = stylish.render(nested.diff)
    assert got == expected, 'nested failed'


def test_plain_view(simple, nested):

    expected = simple.res_plain
    got = plain.render(simple.diff)
    assert got == expected

    expected = nested.res_plain
    got = plain.render(nested.diff)
    assert got == expected


def test_json_view(simple, nested):
    got = json.loads(jason.render(simple.diff))
    expected = simple.res_json

    got = json.loads(jason.render(nested.diff))
    expected = nested.res_json
    assert got == expected, 'nested failed'
