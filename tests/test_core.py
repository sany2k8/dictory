import pytest
from types import SimpleNamespace
from dict_utils.core import (
    safely_deep_get,
    has_nested,
    get_all_values_for_key,
    safely_deep_update,
    delete_nested,
    flatten_dict,
    unflatten_dict,
    compact_dict,
    filter_dict,
    invert_dict,
    merge_dicts,
    deep_update,
    dict_diff,
    dict_depth,
    dict_to_object,
    object_to_dict,
    nested_keys,
    replace_keys,
    map_dict_values,
)


@pytest.mark.parametrize(
    "data,path,expected",
    [
        ({"a": {"b": {"c": 1}}}, "a.b.c", 1),
        ({"a": [{"b": 5}]}, "a.0.b", 5),
        ({"a": SimpleNamespace(b=10)}, "a.b", 10),
        ({}, "x.y", None),
    ],
)
def test_safely_deep_get(data, path, expected):
    assert safely_deep_get(data, path) == expected


def test_has_nested():
    assert has_nested({"a": {"b": 1}}, "a.b")
    assert not has_nested({"a": {}}, "a.b")


def test_get_all_values_for_key():
    data = {"a": 1, "b": {"a": 2}, "c": [{"a": 3}, {"a": 4}]}
    assert sorted(get_all_values_for_key(data, "a")) == [1, 2, 3, 4]


def test_safely_deep_update():
    d = {}
    safely_deep_update(d, ("a.b.c", 1), ("a.b.d", 2))
    assert d == {"a": {"b": {"c": 1, "d": 2}}}


def test_delete_nested():
    d = {"a": {"b": {"c": 1}}}
    delete_nested(d, "a.b.c")
    assert d == {"a": {"b": {}}}


def test_flatten_dict():
    assert flatten_dict({"a": {"b": 1}}) == {"a.b": 1}


def test_unflatten_dict():
    assert unflatten_dict({"a.b": 1}) == {"a": {"b": 1}}


def test_compact_dict():
    assert compact_dict({"a": None, "b": 1, "c": {}, "d": ""}) == {"b": 1}


def test_filter_dict():
    assert filter_dict({"a": 1, "b": 2}, {"a"}) == {"a": 1}


def test_invert_dict():
    assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_merge_dicts():
    assert merge_dicts({"a": {"b": 1}}, {"a": {"c": 2}}) == {"a": {"b": 1, "c": 2}}


def test_deep_update():
    assert deep_update({"a": {"b": 1}}, {"a": {"c": 2}}) == {"a": {"b": 1, "c": 2}}


def test_dict_diff():
    assert dict_diff({"a": 1}, {"a": 2, "b": 3}) == {
        "added": {"b": 3},
        "removed": {},
        "changed": {"a": (1, 2)},
    }


def test_dict_depth():
    assert dict_depth({"a": {"b": {"c": 1}}}) == 3


def test_dict_to_object_and_back():
    d = {"a": {"b": 1}}
    obj = dict_to_object(d)
    assert isinstance(obj, SimpleNamespace)
    assert object_to_dict(obj) == d


def test_nested_keys():
    assert nested_keys({"a": {"b": 1}, "c": 2}) == ["a", "a.b", "c"]


def test_replace_keys():
    assert replace_keys({"a": {"b": 1}}, lambda k: k.upper()) == {"A": {"B": 1}}


def test_map_dict_values():
    assert map_dict_values({"a": 1, "b": {"c": 2}}, lambda v: v * 10) == {
        "a": 10,
        "b": {"c": 20},
    }
