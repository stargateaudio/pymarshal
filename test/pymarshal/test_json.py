"""

"""

import pytest

from pymarshal.json import *


def test_marshal_json():
    class DummyClass:
        _marshal_exclude = ['d']
        def __init__(self):
            pass

    obj = DummyClass()
    obj.a = DummyClass()
    obj.d = 20  # should not be in output
    obj.a.b = 5
    obj.a.d = 50  # should not be in output
    obj.e = (1, 2, 3)

    j = marshal_json(obj)
    assert j == {
        'a': {'b': 5},
        'e': (1, 2, 3),
    }, j


def test_marshal_json_marshal_only_init_args_true():
    class DummyClass:
        _marshal_only_init_args = True
        def __init__(self, a):
            self.a = a
            self.b = 50 # should be ignored

    obj = DummyClass(10)
    j = marshal_json(obj)
    assert j == {'a': 10}


def test_marshal_json_marshal_exclude_and_only_init_args():
    class DummyClass:
        _marshal_exclude = ['b']
        _marshal_only_init_args = True
        def __init__(self, a, b):
            self.a = a
            self.b = b

    obj = DummyClass(10, 20)
    j = marshal_json(obj)
    assert j == {'a': 10}


def test_marshal_json_marshal_exclude_none():
    class DummyClass:
        _marshal_exclude_none = True
        def __init__(self, a):
            self.a = a
            self.b = None # should be ignored

    obj = DummyClass(10)
    j = marshal_json(obj)
    assert j == {'a': 10}


def test_marshal_json_marshal_exclude_none_keys():
    class DummyClass:
        _marshal_exclude_none_keys = [
            'b',
        ]
        def __init__(self, a):
            self.a = a
            self.b = None # should be ignored
            self.c = None

    obj = DummyClass(10)
    j = marshal_json(obj)
    assert j == {'a': 10, 'c': None}


def test_marshal_json_fields():
    class DummyClass:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, int)
    c = DummyClass(1, 2)
    j = marshal_json(c, fields=['a'])
    assert j == {'a': 1}


def test_unmarshal_json():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, TestClassB)

    class TestClassB:
        def __init__(self, b):
            self.b = type_assert(b, float)


    obj = unmarshal_json(
        {'a': 5, 'b': {'b': 10.2, 'c': 4.5}}, # 'c' should be ignored
        TestClassA,
    )
    assert obj.a == 5
    assert obj.b.b == 10.2
    assert not hasattr(obj.b, 'c')


def test_unmarshal_json_raises_extra_keys_error():
    class TestClassA:
        def __init__(self, a):
            self.a = type_assert(a, int)

    with pytest.raises(ExtraKeysError):
        unmarshal_json(
            {'a': 5, 'b': 2},
            TestClassA,
            allow_extra_keys=False,
        )


def test_unmarshal_json_raises_extra_keys_error_from_cls():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, TestClassB)

    class TestClassB:
        _unmarshal_allow_extra_keys = False

        def __init__(self, c):
            self.c = type_assert(c, float)

    with pytest.raises(ExtraKeysError):
        unmarshal_json(
            {'a': 5, 'b': {'c': 4.5, 'd': 2.4}},
            TestClassA,
            allow_extra_keys=True,
        )


def test_unmarshal_json_raises_init_args_error():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, int)

    with pytest.raises(InitArgsError):
        unmarshal_json(
            {'a': 5, 'b': 'd'},
            TestClassA,
            allow_extra_keys=True,
        )


def test_unmarshal_json_allow_extra_keys():
    class TestClassA:
        def __init__(self, a):
            self.a = type_assert(a, int)

    obj = unmarshal_json(
        {'a': 5, 'b': 2},
        TestClassA,
        allow_extra_keys=True,
    )

    assert obj.a == 5
    assert not hasattr(obj, 'b')


def test_unmarshal_json_factory_function():
    class TestClassA:
        def __init__(self, a, b):
            self.a = type_assert(a, str)
            self.b = type_assert(b, str)

    def factory(a, b):
        return TestClassA(
            str(a),
            str(b),
        )

    t = unmarshal_json({'a': 1, 'b': 2}, factory)
    assert t.a == '1'
    assert t.b == '2'


def test_marshal_slots():
    class Test:
        __slots__ = ['a', 'b']
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, int)

        def method(self):
            pass

    t = Test(1, 2)
    j = marshal_json(t)
    assert j['a'] == 1
    assert j['b'] == 2

    t2 = unmarshal_json(j, Test)
    assert t.a == 1
    assert t.b == 2


def test_unmarshal_ctor():
    class A:
        def __init__(self, a, b):
            self.a = type_assert(a, int)
            self.b = type_assert(b, B, ctor=B.factory)

    class B:
        def __init__(self, c, d):
            self.c = type_assert(c, int)
            self.d = type_assert(d, int)

        @staticmethod
        def factory(c):
            return B(c, c+c)

    d = {'a': 6, 'b': {'c': 10, 'b': 50}}
    a = unmarshal_json(d, A)
    assert a.b.d == 20

def test_marshal_json_list():
    class A:
        def __init__(self, a, b):
            self.a = type_assert(a, str)
            self.b = type_assert(b, int)

    class B:
        def __init__(self, a):
            self.a = type_assert_iter(a, A)

    obj = B([
        A("a", 1),
        A("b", 2),
    ])
    j = marshal_json(obj)
    assert j == {
        'a': [
            {'a': 'a', 'b': 1},
            {'a': 'b', 'b': 2}
        ]
    }

def test_marshal_json_dict():
    class A:
        def __init__(self, a, b):
            self.a = type_assert(a, str)
            self.b = type_assert(b, int)

    class B:
        def __init__(self, a):
            self.a = type_assert_dict(a, vcls=A)

    obj = B({
        'a': A("a", 1),
        'b': A("b", 2),
    })
    j = marshal_json(obj)
    assert j == {
        'a': {
            'a': {'a': 'a', 'b': 1},
            'b': {'a': 'b', 'b': 2}
        }
    }

def test_marshal_list_of_ints():
    class A:
        def __init__(self, a):
            self.a = a
    obj = A([1, 2, 3])
    j = marshal_json(obj)
    assert j == {'a': [1, 2, 3]}, j

