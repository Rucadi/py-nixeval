import nixeval

# Parse a Nix list into Python
data = nixeval.loads('[ 1 2 3 ]')
assert data == [1,2,3]

# Parse a Nix attribute set into Python dict
config = nixeval.loads('{ foo = "bar"; baz = [ true false ]; }')
print(config)
# {'baz': [True, False], 'foo': 'bar'}