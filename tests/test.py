from gendiff.scripts.core import generate_diff


def test_generate_diff():
    f = open('./tests/fixtures/gendiff_result.txt')
    right_answer = f.read()

    answer = (generate_diff(
        './tests/fixtures/before.json', './tests/fixtures/after.json'))
    assert(answer == right_answer)


test_generate_diff()
