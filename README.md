# py-nixeval

Python bindings for evaluating and round‑tripping Nix expressions, powered by \[snix\_eval] and \[PyO3].

## Features

* **Parse Nix expressions** into native Python objects.
* **Serialize Python objects** to JSON then convert back into Nix values using
* **Windows support** Nix is usually not seen in windows, but thanks to tvix/snix projects now you can use it on windows
* **Seamless round‑trip** between Nix and Python data structures.

## Limitations

The implementation internally relies on the python json module and on nix features builtins.toJSON and builtins.fromJSON, this means that an unevaluated lambda in the result will not work.  
## Installation

Install from PyPI:

```bash
pip install py-nixeval
```

Or test it from source:

```bash
git clone https://github.com/yourusername/py-nixeval.git
cd py-nixeval
nix-shell
maturin develop --release
```

## Quickstart

```python
import nixeval

# Parse a Nix list into Python
data = nixeval.loads('[ 1 2 3 ]')
assert data == [1,2,3]

# Parse a Nix attribute set into Python dict
config = nixeval.loads('{ foo = "bar"; baz = [ true false ]; }')
print(config)
# {'baz': [True, False], 'foo': 'bar'}
```
