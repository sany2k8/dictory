from typing import Any, Union, Callable, List
from types import SimpleNamespace


# Access utilities


def safely_deep_get(
    dictionary: Union[dict, list, tuple], keys: str, default: Any = None
) -> Any:
    """
    Safely retrieve a value from a nested dictionary or list using a dot-separated key path.

    Args:
        dictionary (Union[dict, list, tuple]): The dictionary, list, or tuple to search.
        keys (str): The dot-separated key path to the desired value.
        default (Any, optional): The default value to return if the key is not found. Defaults to None.

    Returns:
        Any: The value associated with the key path, or the default value if the key is not found.
    """
    node = dictionary
    for key in keys.split("."):
        if isinstance(node, dict):
            node = node.get(key, default)
        elif isinstance(node, (list, tuple)):
            if key.isdigit():
                index = int(key)
                if 0 <= index < len(node):
                    node = node[index]
                else:
                    return default
            else:
                return default
        elif hasattr(node, key):
            node = getattr(node, key, default)
        else:
            return default
    return node


def has_nested(d, path):
    """
    Check if a nested key exists in a dictionary or list.

    Args:
        d (dict): The dictionary to search.
        path (str): The dot-separated key path to check.

    Returns:
        bool: True if the key exists, False otherwise.
    """
    keys = path.split(".")
    current = d
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif hasattr(current, key):
            current = getattr(current, key)
        elif isinstance(current, list) and key.isdigit() and int(key) < len(current):
            current = current[int(key)]
        else:
            return False
    return True


def get_all_values_for_key(d: Union[dict, list], key: str) -> List[Any]:
    """
    Recursively retrieve all values associated with a specific key in a nested dictionary or list.

    Args:
        d (Union[dict, list]): The dictionary or list to search.
        key (str): The key to search for.

    Returns:
        List[Any]: A list of values associated with the key.
    """
    results = []
    if isinstance(d, dict):
        for k, v in d.items():
            if k == key:
                results.append(v)
            results.extend(get_all_values_for_key(v, key))
    elif isinstance(d, list):
        for item in d:
            results.extend(get_all_values_for_key(item, key))
    return results


# Update utilities


def safely_deep_update(dictionary: dict, *path_values: tuple[str, Any]) -> dict:
    """
    Safely update a nested dictionary or list using a dot-separated key path.

    Args:
        dictionary (dict): The dictionary to update.
        path_values (tuple[str, Any]): A tuple of (key path, value) pairs to update.

    Returns:
        dict: The updated dictionary.
    """
    for path, value in path_values:
        keys = path.split(".")
        node = dictionary
        for i, key in enumerate(keys):
            is_last = i == len(keys) - 1
            next_key = None if is_last else keys[i + 1]
            if key.isdigit():
                key_int = int(key)  # Use a new variable
                if not isinstance(node, list):
                    raise TypeError("Expected list")
                while len(node) <= key_int:
                    node.append({} if not is_last and not next_key.isdigit() else [])
                if is_last:
                    node[key_int] = value
                else:
                    if not isinstance(node[key_int], (dict, list)):
                        node[key_int] = {} if not next_key.isdigit() else []
                    node = node[key_int]
            else:
                if not isinstance(node, dict):
                    raise TypeError("Expected dict")
                if is_last:
                    node[key] = value
                else:
                    if key not in node or not isinstance(node[key], (dict, list)):
                        node[key] = (
                            {}
                            if next_key is not None and not next_key.isdigit()
                            else []
                        )
                    node = node[key]
    return dictionary


def delete_nested(d: dict, path: str) -> None:
    """
    Delete a nested key from a dictionary or list.

    Args:
        d (dict): The dictionary to delete the key from.
        path (str): The dot-separated key path to delete.
    """
    keys = path.split(".")
    for key in keys[:-1]:
        if isinstance(d, dict):
            d = d.get(key, {})
        elif isinstance(d, list) and key.isdigit():
            idx = int(key)
            d = d[idx] if 0 <= idx < len(d) else {}
    last = keys[-1]
    if isinstance(d, dict):
        d.pop(last, None)
    elif isinstance(d, list) and last.isdigit():
        idx = int(last)
        if 0 <= idx < len(d):
            d[idx] = None


# Transformation utilities


def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """
    Flatten a nested dictionary into a single-level dictionary.

    Args:
        d (dict): The dictionary to flatten.
        parent_key (str, optional): The parent key to use for the flattened dictionary. Defaults to "".
        sep (str, optional): The separator to use between keys. Defaults to ".".

    Returns:
        dict: The flattened dictionary.
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def unflatten_dict(d: dict, sep: str = ".") -> dict:
    """
    Unflatten a flattened dictionary into a nested dictionary.

    Args:
        d (dict): The flattened dictionary to unflatten.
        sep (str, optional): The separator used in the flattened dictionary. Defaults to ".".

    Returns:
        dict: The unflattened dictionary.
    """
    result: dict[str, Any] = {}
    for key, value in d.items():
        keys = key.split(sep)
        ref = result
        for k in keys[:-1]:
            if k not in ref:
                ref[k] = {}
            ref = ref[k]
        ref[keys[-1]] = value
    return result


def compact_dict(d: dict) -> dict:
    """
    Remove empty values from a dictionary.

    Args:
        d (dict): The dictionary to compact.

    Returns:
        dict: The compacted dictionary.
    """
    if not isinstance(d, dict):
        return d
    return {k: compact_dict(v) for k, v in d.items() if v not in (None, [], {}, "")}


def filter_dict(d: dict, keys_to_keep: set) -> dict:
    """
    Filter a dictionary to only include specified keys.

    Args:
        d (dict): The dictionary to filter.
        keys_to_keep (set): The set of keys to keep.

    Returns:
        dict: The filtered dictionary.
    """
    return {k: v for k, v in d.items() if k in keys_to_keep}


def invert_dict(d: dict) -> dict:
    """
    Invert a dictionary, swapping keys and values.

    Args:
        d (dict): The dictionary to invert.

    Returns:
        dict: The inverted dictionary.
    """
    return {v: k for k, v in d.items() if hashable(v)}


def hashable(v: Any) -> bool:
    """
    Check if a value is hashable.

    Args:
        v (Any): The value to check.

    Returns:
        bool: True if the value is hashable, False otherwise.
    """
    try:
        hash(v)
        return True
    except TypeError:
        return False


# Merge utilities


def merge_dicts(d1: dict, d2: dict) -> dict:
    """
    Merge two dictionaries recursively.

    Args:
        d1 (dict): The first dictionary to merge.
        d2 (dict): The second dictionary to merge.

    Returns:
        dict: The merged dictionary.
    """
    result = d1.copy()
    for k, v in d2.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = merge_dicts(result[k], v)
        else:
            result[k] = v
    return result


def deep_update(d: dict, u: dict) -> dict:
    """
    Update a dictionary recursively.

    Args:
        d (dict): The dictionary to update.
        u (dict): The dictionary containing the updates.

    Returns:
        dict: The updated dictionary.
    """
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def dict_diff(d1: dict, d2: dict) -> dict:
    """
    Calculate the difference between two dictionaries.

    Args:
        d1 (dict): The first dictionary.
        d2 (dict): The second dictionary.

    Returns:
        dict: A dictionary containing the added, removed, and changed keys.
    """
    diff = {
        "added": {k: d2[k] for k in d2 if k not in d1},
        "removed": {k: d1[k] for k in d1 if k not in d2},
        "changed": {k: (d1[k], d2[k]) for k in d1 if k in d2 and d1[k] != d2[k]},
    }
    return diff


def dict_depth(d: dict) -> int:
    """
    Calculate the depth of a dictionary.

    Args:
        d (dict): The dictionary to calculate the depth of.

    Returns:
        int: The depth of the dictionary.
    """
    if not isinstance(d, dict) or not d:
        return 0
    return 1 + max(
        (dict_depth(v) for v in d.values() if isinstance(v, dict)), default=0
    )


# Conversion


def dict_to_object(d: dict) -> SimpleNamespace:
    """
    Convert a dictionary to a SimpleNamespace.

    Args:
        d (dict): The dictionary to convert.

    Returns:
        SimpleNamespace: The converted SimpleNamespace.
    """
    return SimpleNamespace(
        **{k: dict_to_object(v) if isinstance(v, dict) else v for k, v in d.items()}
    )


def object_to_dict(obj: Any) -> dict:
    """
    Convert a SimpleNamespace to a dictionary.

    Args:
        obj (Any): The SimpleNamespace to convert.

    Returns:
        dict: The converted dictionary.
    """
    if isinstance(obj, SimpleNamespace):
        return {k: object_to_dict(v) for k, v in vars(obj).items()}
    return obj


def nested_keys(d: dict, prefix="") -> List[str]:
    """
    Retrieve all nested keys from a dictionary.

    Args:
        d (dict): The dictionary to retrieve keys from.
        prefix (str, optional): The prefix to use for the keys. Defaults to "".

    Returns:
        List[str]: A list of nested keys.
    """
    keys = []
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        keys.append(full_key)
        if isinstance(v, dict):
            keys.extend(nested_keys(v, full_key))
    return keys


def replace_keys(d: dict, replace_fn: Callable[[str], str]) -> dict:
    """
    Replace all keys in a dictionary using a function.

    Args:
        d (dict): The dictionary to replace keys in.
        replace_fn (Callable[[str], str]): The function to use to replace keys.

    Returns:
        dict: The dictionary with replaced keys.
    """
    return {
        replace_fn(k): replace_keys(v, replace_fn) if isinstance(v, dict) else v
        for k, v in d.items()
    }


def map_dict_values(d: dict, map_fn: Callable[[Any], Any]) -> dict:
    """
    Map all values in a dictionary using a function.

    Args:
        d (dict): The dictionary to map values in.
        map_fn (Callable[[Any], Any]): The function to use to map values.

    Returns:
        dict: The dictionary with mapped values.
    """
    return {
        k: map_dict_values(v, map_fn) if isinstance(v, dict) else map_fn(v)
        for k, v in d.items()
    }
