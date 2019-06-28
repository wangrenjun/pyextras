#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'reversed_dict',
    'ConstDotDictify',
    'floatify',
    'align_size',
    'roundup',
    'get_terminal_size',
    'xstr',
    'make_list_of_dict_from_arrays',
    'has_all_keys',
    'has_any_keys',
    'joiniterable',
    'transposelist',
    'RingLooper',
    'urlscheme',
    'cut_integer',
    'count_set_bits',
    'isv2',
    'isv3',
    'inversed_textwrap',
    'streamistty',
    'fuzzy_match',
    'substr_match',
    'has_fuzzy_matched',
    'has_substr_matched',
]

import math, os, sys, itertools, urllib, difflib

# Swap keys for values
reversed_dict = lambda d: dict(zip(d.values(), d.keys()))

class ConstDotDictify():
    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
    def __getitem__(self, key):
        return self.__dict__[key]
    __getattr__ = __getitem__
    def __readonly__(self, *args, **kwargs):
        raise AttributeError("Cannot reassign members.")
    __setattr__ = __readonly__
    __setitem__ = __readonly__
    del __readonly__

def floatify(s):
    try:
        return float(s)
    except ValueError:
        return s

# Only to be used to align on a power of 2 boundary.
align_size = lambda size, boundary: size + (boundary - 1) & ~(boundary - 1) if math.log(boundary, 2).is_integer() else None

roundup = lambda n, b: int(math.ceil(n / b)) * b

def get_terminal_size(file = sys.stdout):
    try:
        _ = os.get_terminal_size(file.fileno())
        columns, lines = _.columns, _.lines
    except OSError:
        columns, lines = 0, 0
    return columns, lines

# Convert None, 0, False, or any falsy value to empty string.
xstr = lambda s: str(s or '')

def make_list_of_dict_from_arrays(keys, *values):
    l = []
    if keys:
        for i in [[[k, v] for k, v in zip(keys, vals)] for vals in values ]:
            l.append(dict(i))
    return l

has_all_keys = lambda dict, keys: all(_ in dict for _ in keys)
has_any_keys = lambda dict, keys: any(_ in dict for _ in keys)

joiniterable = lambda sep, seq: sep.join(map(str, seq))

transposelist = lambda l: list(map(list, zip(*l)))

class RingLooper():
    def __init__(self, *array):
        self.__array = array
    def __iter__(self):
        self.__cycler = itertools.cycle(range(len(self.__array)))
        return self
    def __next__(self):
        if self.__array:
            return self.__array[next(self.__cycler)]
        else:
            raise StopIteration

urlscheme = lambda url: urllib.parse.urlparse(url).scheme

cut_integer = lambda num, bits: num & ((1<< bits) - 1)

def count_set_bits(n):
    count = 0
    while (n):
        n = n & (n - 1)
        count += 1
    return count

isv2 = lambda : True if sys.version_info[0] == 2 else False
isv3 = lambda : True if sys.version_info[0] == 3 else False

"""
>>> inversed_textwrap('1234567890', 3)
['1', '234', '567', '890']
"""
inversed_textwrap = lambda text, wrapwidth: list(map(lambda x:x[::-1], textwrap.wrap(text[::-1], wrapwidth)[::-1]))

# Check filestream is attached to terminal.
streamistty = lambda file: True if file.isatty() else False

DEFAULT_THRESHOLD = 0.7

def fuzzy_match(needle, haystack, ignore_case = False, threshold = DEFAULT_THRESHOLD):
    if ignore_case:
        matching = lambda entry: difflib.SequenceMatcher(a = needle.lower(), b = entry.lower()).ratio() >= threshold
    else:
        matching = lambda entry: difflib.SequenceMatcher(a = needle, b = entry).ratio() >= threshold
    return filter(match, haystack)

def substr_match(needle, haystack, ignore_case = False):
    if ignore_case:
        matching = lambda entry: needle.lower() in entry.lower()
    else:
        matching = lambda entry: needle in entry
    return filter(match, haystack)

def has_fuzzy_matched(needle, haystack, ignore_case = False, threshold = DEFAULT_THRESHOLD):
    if ignore_case:
        matching = lambda entry: difflib.SequenceMatcher(a = needle.lower(), b = entry.lower()).ratio() >= threshold
    else:
        matching = lambda entry: difflib.SequenceMatcher(a = needle, b = entry).ratio() >= threshold
    for entry in haystack:
        if matching(entry):
            return True
    return False

def has_substr_matched(needle, haystack, ignore_case = False):
    if ignore_case:
        matching = lambda entry: needle.lower() in entry.lower()
    else:
        matching = lambda entry: needle in entry
    for entry in haystack:
        if matching(entry):
            return True
    return False
