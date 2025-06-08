from typing import Any, Union, Callable, List, Dict
from types import SimpleNamespace


# Access utilities


def safely_deep_get(
    dictionary: Union[dict, list, tuple], keys: str, default: Any = None
) -> Any:
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


def has_nested(dictionary: Union[dict, list], path: str) -> bool:
    return safely_deep_get(dictionary, path, object()) is not object()


def get_all_values_for_key(d: Union[dict, list], key: str) -> List[Any]:
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
    for path, value in path_values:
        keys = path.split(".")
        node = dictionary
        for i, key in enumerate(keys):
            is_last = i == len(keys) - 1
            next_key = None if is_last else keys[i + 1]
            if key.isdigit():
                key = int(key)
                if not isinstance(node, list):
                    raise TypeError("Expected list")
                while len(node) <= key:
                    node.append({} if not is_last and not next_key.isdigit() else [])
                if is_last:
                    node[key] = value
                else:
                    if not isinstance(node[key], (dict, list)):
                        node[key] = {} if not next_key.isdigit() else []
                    node = node[key]
            else:
                if not isinstance(node, dict):
                    raise TypeError("Expected dict")
                if is_last:
                    node[key] = value
                else:
                    if key not in node or not isinstance(node[key], (dict, list)):
                        node[key] = {} if not next_key.isdigit() else []
                    node = node[key]
    return dictionary


def delete_nested(d: dict, path: str) -> None:
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
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def unflatten_dict(d: dict, sep: str = ".") -> dict:
    result = {}
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
    if not isinstance(d, dict):
        return d
    return {k: compact_dict(v) for k, v in d.items() if v not in (None, [], {}, "")}


def filter_dict(d: dict, keys_to_keep: set) -> dict:
    return {k: v for k, v in d.items() if k in keys_to_keep}


def invert_dict(d: dict) -> dict:
    return {v: k for k, v in d.items() if hashable(v)}


def hashable(v: Any) -> bool:
    try:
        hash(v)
        return True
    except TypeError:
        return False


# Merge utilities


def merge_dicts(d1: dict, d2: dict) -> dict:
    result = d1.copy()
    for k, v in d2.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = merge_dicts(result[k], v)
        else:
            result[k] = v
    return result


def deep_update(d: dict, u: dict) -> dict:
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def dict_diff(d1: dict, d2: dict) -> dict:
    diff = {
        "added": {k: d2[k] for k in d2 if k not in d1},
        "removed": {k: d1[k] for k in d1 if k not in d2},
        "changed": {k: (d1[k], d2[k]) for k in d1 if k in d2 and d1[k] != d2[k]},
    }
    return diff


def dict_depth(d: dict) -> int:
    if not isinstance(d, dict) or not d:
        return 0
    return 1 + max(
        (dict_depth(v) for v in d.values() if isinstance(v, dict)), default=0
    )


# Conversion


def dict_to_object(d: dict) -> SimpleNamespace:
    return SimpleNamespace(
        **{k: dict_to_object(v) if isinstance(v, dict) else v for k, v in d.items()}
    )


def object_to_dict(obj: Any) -> dict:
    if isinstance(obj, SimpleNamespace):
        return {k: object_to_dict(v) for k, v in vars(obj).items()}
    return obj


def nested_keys(d: dict, prefix="") -> List[str]:
    keys = []
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        keys.append(full_key)
        if isinstance(v, dict):
            keys.extend(nested_keys(v, full_key))
    return keys


def replace_keys(d: dict, replace_fn: Callable[[str], str]) -> dict:
    return {
        replace_fn(k): replace_keys(v, replace_fn) if isinstance(v, dict) else v
        for k, v in d.items()
    }


def map_dict_values(d: dict, map_fn: Callable[[Any], Any]) -> dict:
    return {
        k: map_dict_values(v, map_fn) if isinstance(v, dict) else map_fn(v)
        for k, v in d.items()
    }
