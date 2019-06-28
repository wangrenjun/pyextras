#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'humanizedbin',
    'humanizedtwoscompbin',
    'humanizedoct',
    'humanizedhex',
    'humanizeddec',
    'humanizedbinip',
]

import textwrap, ipaddress
from utils import inversed_textwrap
from utils import cut_integer

def humanizedbin(num, wrapwidth = 4, sep = ' '):
    if num < 0:
        sign = '-'
        s = '{:b}'.format(num)[1:]
    else:
        sign = ''
        s = '{:b}'.format(num)
    return '%s%s' % (sign, sep.join(textwrap.wrap(s.zfill(roundup(len(s), wrapwidth)), wrapwidth)))

# Format two's complement representation
def humanizedtwoscompbin(num, bits = 32, wrapwidth = 4, sep = ' '):
    s = '{:b}'.format(cut_integer(num, bits))
    return '%s' % (sep.join(textwrap.wrap(s.zfill(bits), wrapwidth)))

def humanizedoct(num, wrapwidth = 3, sep = ' '):
    if num < 0:
        sign = '-'
        s = '{:o}'.format(num)[1:]
    else:
        sign = ''
        s = '{:o}'.format(num)
    return '%s%s' % (sign, sep.join(inversed_textwrap(s, wrapwidth)))

def humanizedhex(num, wrapwidth = 4, sep = ' ', with_capitals = True):
    if num < 0:
        sign = '-'
        s = '{:{type}}'.format(num, type = 'X' if with_capitals else 'x')[1:]
    else:
        sign = ''
        s = '{:{type}}'.format(num, type = 'X' if with_capitals else 'x')
    return '%s%s' % (sign, sep.join(inversed_textwrap(s, wrapwidth)))

def humanizeddec(num, wrapwidth = 3, sep = ','):
    if num < 0:
        sign = '-'
        s = '{:d}'.format(num)[1:]
    else:
        sign = ''
        s = '{:d}'.format(num)
    return '%s%s' % (sign, sep.join(inversed_textwrap(s, wrapwidth)))

def humanizedbinip(ipaddr):
    if ipaddr.version == 4:
        fillwidth = 32
        wrapwidth = 8
    else:
        fillwidth = 128
        wrapwidth = 16
    return '.'.join(textwrap.wrap('{:b}'.format(int(ipaddr)).zfill(fillwidth), wrapwidth))
