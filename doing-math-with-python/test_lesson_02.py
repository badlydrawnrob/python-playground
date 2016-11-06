from lesson_02 import is_float


def test_is_float():
    assert is_float(3.5) == 3.5
    assert is_float(3) == 'Definitely not a float'
