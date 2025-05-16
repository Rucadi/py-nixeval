import pytest
import nixeval
import json


def assert_equivalent(result, expected):
    """Helper to compare nested structures, using JSON canonicalization when dicts are involved."""
    if isinstance(expected, dict):
        # Compare dicts (including nested) by JSON with sorted keys
        assert json.dumps(result, sort_keys=True) == json.dumps(expected, sort_keys=True)
    else:
        assert result == expected


@pytest.mark.parametrize("expr,expected", [
    ('"hello"', "hello"),
    ('42', 42),
    ('3.14', 3.14),
    ('[1 2 3]', [1, 2, 3]),
    ('{ foo = "bar"; baz = 100; }', {'foo': 'bar', 'baz': 100}),
])
def test_loads_valid(expr, expected):
    """
    loads() should correctly parse valid Nix expressions to Python objects.
    """
    result = nixeval.loads(expr)
    assert_equivalent(result, expected)


def test_loads_invalid():
    """
    loads() should raise ValueError on invalid Nix expression.
    """
    with pytest.raises(ValueError):
        nixeval.loads('invalidnix!')


@pytest.mark.parametrize("obj", [
    "hello",
    123,
    3.14,
    [1, 2, {'x': 'y'}],
    {'a': 1, 'b': [True, False, None]},
])
def test_dumps_roundtrip(obj):
    """
    dumps() should produce a Nix expression that, when loaded, returns the original object.
    """
    nix_expr = nixeval.dumps(obj)
    result = nixeval.loads(nix_expr)
    assert result == obj


def test_dumps_type_error():
    """
    dumps() should raise a TypeError when given a non-serializable object.
    """
    class Unserializable:
        pass

    with pytest.raises(TypeError):
        nixeval.dumps(Unserializable())
