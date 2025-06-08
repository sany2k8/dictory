# dictory

A playful blend of "dict" and "utility/library".

## Overview

`dictory` is a Python package providing useful utilities to work with Python dictionaries.  
It aims to simplify common dictionary operations and improve your productivity when dealing with nested dicts, mapping, merging, and more.

## Features

- Utilities for nested dictionary manipulation
- Safe get/set operations
- Dict merging and diffing
- Conversion helpers

## Installation

Using `pip`,

```bash
pip install .
# or for development:
pip install -e .
```

Using `uv`,

```bash
uv pip install .
# or for development:
uv pip install -e .
```


## Usage

```python
from dictory import dict_utils

# Example: Safe get from nested dict
nested = {"a": {"b": {"c": 123}}}
result = dict_utils.get_nested(nested, ["a", "b", "c"])  # 123

# Example: Merge two dicts
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = dict_utils.merge_dicts(d1, d2)  # {'a': 1, 'b': 3, 'c': 4}
```

## Development

Install developer dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest
```

## License

MIT License
