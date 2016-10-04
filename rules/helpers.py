# coding: utf-8
from __future__ import unicode_literals, absolute_import

_NOTSET = type(
    b"NotSet",
    (object,),
    {"__repr__": lambda self: "<ValueNotSet>"}
)()


def get_by_path(keys, source_dict):
    if "." in keys:
        key, tail_keys = keys.split(".", 1)
        if key not in source_dict:
            return _NOTSET
        return get_by_path(tail_keys, source_dict[key])
    else:
        return source_dict.get(keys, _NOTSET)