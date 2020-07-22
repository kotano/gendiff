from gendiff.views import default_view


def test_default_view(
        simple_difference, simple_res,
        nested_difference, nested_res):
    expected = simple_res
    got = default_view(simple_difference)
    assert got == expected

    expected = nested_res
    got = default_view(nested_difference)
    assert got == expected
