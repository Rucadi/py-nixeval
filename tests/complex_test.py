import pytest
import nixeval
import json

def assert_equivalent(result, expected):
    """Helper to compare nested structures, using JSON canonicalization when dicts are involved."""
    if isinstance(expected, dict):
        assert json.dumps(result, sort_keys=True) == json.dumps(expected, sort_keys=True)
    else:
        assert result == expected


@pytest.mark.parametrize("expr,expected", [
    # simple primitives
    ('true', True),
    ('false', False),
    ('null', None),

    # integer edge‑cases
    ('0', 0),
    ('-42', -42),
    ('123', 123),

    # strings with escapes & multi‑line
     (r'"line1\nline2"', "line1\nline2"),
     ('''"multi\nline\nstring"''', "multi\nline\nstring"),  # if nixeval supports block‑strings

    # lists, including empty and nested
    ('[]', []),
    ('[  1   2   [3 4]  ]', [1, 2, [3, 4]]),

    # attribute sets with nesting, formatting, comments
    (
        '''
        {
          # simple comment
          foo = "bar"; 
          nested = { x = 1; y = [ true false null ]; };
        }
        ''',
        {'foo': 'bar', 'nested': {'x': 1, 'y': [True, False, None]}}
    ),

    # mixed types
    (
        '{ a = [1 { b = [2 3]; }]; c = false; }',
        {'a': [1, {'b': [2, 3]}], 'c': False}
    ),

])
def test_loads_interesting(expr, expected):
    """loads() handles booleans, null, escapes, nesting, comments, etc."""
    result = nixeval.loads(expr)
    assert_equivalent(result, expected)


@pytest.mark.parametrize("obj", [
    # primitives
    True, False, None,
    -99, 0, 999999999999,
    0.0001, 3.14159, 10000000,

    # strings with tricky characters
    "simple",
    "with\nnewline",
    "quote: \" and backslash: \\",

    # nested lists and dicts
    [[], [[], [1, 2, 3]], {}],
    {'empty': {}, 'list': [], 'mixed': [1, {"a": True}, None]},

    # deeper nesting
    {'level1': {'level2': {'level3': [1, {'x':'y'}, [True, False, None]]}}},

])
def test_dumps_roundtrip_interesting(obj):
    """Round-trip dumps->loads should preserve even tricky values."""
    nix_expr = nixeval.dumps(obj)
    loaded = nixeval.loads(nix_expr)
    assert loaded == obj


def test_dumps_invalid_type():
    """Ensure TypeError on unserializable objects."""
    class Weird:
        def __repr__(self):
            return "<weird>"

    with pytest.raises(TypeError):
        nixeval.dumps(Weird())
