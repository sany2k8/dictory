# Dictory

A playful blend of "dict" and "utility/library".

## Overview

`dictory` is a Python package providing useful utilities to work with Python dictionaries. It aims to simplify common dictionary operations and improve your productivity when dealing with nested dicts, mapping, merging, and more.

## Features

<!-- - Utilities for nested dictionary manipulation -->
- Safe get/set/update/delete operations.
- Dict merging and diffing.
- Conversion helpers.
- Flattening and unflattening dictionaries.
- Type checking and validation.
- Customizable key transformations.
- Support for nested structures.
- Efficient handling of large dictionaries.
- Performance optimizations for common operations.

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
result = dict_utils.safely_deep_get(nested, "a.b.c")  # 123

# Example: Check if a nested key exists
nested = {"a": {"b": {"c": 123}}}
exists = dict_utils.has_nested(nested, "a.b.c")  # True

# Example : safely deep update a nested dict
nested = {"a": {"b": {"c": 123}}}
dict_utils.safely_deep_update(nested, {"a": {"b": {"d": 456}}})
# nested is now {"a": {"b": {"c": 123, "d": 456}}}


# Example: Delete a nested key
nested = {"a": {"b": {"c": 123}}}
dict_utils.delete_nested(nested, "a.b.c")
# nested is now {"a": {"b": {}}}

# Example: flatten_dict 
flat = dict_utils.flatten_dict({"a": {"b": {"c": 123}}})
# flat is now {"a.b.c": 123}        
```

## Development

Install developer dependencies:

```bash
uv sync --extra dev
```

Run tests:

```bash
uv run pytest
```

## License

MIT License

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Authors
- [Sany Ahmed](https://github.com/sany2k8)
- [Contributors](https://github.com/your-username/dictory/graphs/contributors)


## Acknowledgements
This project was inspired by the need for more efficient dictionary manipulation in Python. Thanks to the open-source community for their contributions and support.
