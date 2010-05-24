#!/usr/bin/env python
# vim: et ts=4 sw=4


import copy


def extract(query_dict, prefix=""):
    """
    Extract the *order_by*, *per_page*, and *page* parameters from
    `query_dict` (a Django QueryDict), and return a dict suitable for
    instantiating a preconfigured Table object.
    """

    strs = ['order_by']
    ints = ['per_page', 'page']

    extracted = { }

    for key in (strs + ints):
        if (prefix + key) in query_dict:
            val = query_dict.get(prefix + key)

            extracted[key] = (val
                if not key in ints
                else int(val))

    return extracted


def build(path, query_dict, prefix="", **kwargs):
    """
    """

    query_dict = _copy(
        query_dict)

    for key in kwargs:
        query_dict[prefix + key] = kwargs[key]

    return "%s?%s" % (path, query_dict.urlencode())\
        if query_dict else path


def _copy(query_dict):
    """
    Return a mutable copy of `query_dict`. This is a workaround to
    Django bug #13572, which prevents QueryDict.copy from working.
    """

    memo = { }

    result = query_dict.__class__('',
        encoding=query_dict.encoding,
        mutable=True)

    memo[id(query_dict)] = result

    for key, value in dict.items(query_dict):
        dict.__setitem__(result,
            copy.deepcopy(key, memo),
            copy.deepcopy(value, memo))

    return result
