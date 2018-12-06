import pytest

from homework02 import callstat


def test_call_count():

    @callstat
    def test_fn(*args, **kwargs):
        return locals()

    assert test_fn.call_count == 0

    args = (1, 2)
    kwargs = {'a': 3}
    res = test_fn(*args, **kwargs)

    assert res == {'args': args, 'kwargs': kwargs},\
        'Декоратор некорректно обрабатывает возвращаемое значение функции'

    assert test_fn.call_count == 1

    test_fn()
    test_fn()

    assert test_fn.call_count == 3

    with pytest.raises(Exception):
        test_fn.call_count = 100