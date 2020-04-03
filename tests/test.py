from gendiff.scripts.core import generate_diff


def test_generate_diff():
    right_answer = '''{
    host : hexlet.io
  - proxy : 123.234.53.22
  + timeout : 20
  - timeout : 50
  + verbose : True
}'''

    answer = (generate_diff(
        './fixtures/before.json', './fixtures/after.json'))
    # '../../tests/fixtures/before.json', '../../tests/fixtures/after.json'))
    assert(answer == right_answer)


test_generate_diff()
