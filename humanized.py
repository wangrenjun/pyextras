#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'humanizedbin',
    'humanizedtwoscompbin',
    'humanizedoct',
    'humanizedhex',
    'humanizeddec',
    'humanizedbinip',
    'humanizedbytes',
    'humanizedpercentage',
    'humanizedpercentage2',
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

__capacity_symbols = {
    'traditionalbytes' : (
    ('YB',  'yottabyte',    10 ** 24    ),
    ('ZB',  'zetabyte',     10 ** 21    ),
    ('EB',  'exabyte',      10 ** 18    ),
    ('PB',  'petabyte',     10 ** 15    ),
    ('TB',  'terabyte',     10 ** 12    ),
    ('GB',  'gigabyte',     10 ** 9     ),
    ('MB',  'megabyte',     10 ** 6     ),
    ('kB',  'kilobyte',     10 ** 3     ),),
    'iecbytes' : (
    ('YiB', 'yobibyte',     1 << 80     ),
    ('ZiB', 'zebibyte',     1 << 70     ),
    ('EiB', 'exbibyte',     1 << 60     ),
    ('PiB', 'pebibyte',     1 << 50     ),
    ('TiB', 'tebibyte',     1 << 40     ),
    ('GiB', 'gibibyte',     1 << 30     ),
    ('MiB', 'mebibyte',     1 << 20     ),
    ('KiB', 'kibibyte',     1 << 10     ),),
}

def humanizedbytes(size, to = 'traditionalbytes', precision = 1):
    if isinstance(size, (int, float)):
        if size < 0:
            raise ValueError('size < 0')
        bytes = size
    elif isinstance(size, str):
        for name, symbols in __capacity_symbols.items():
            for item in symbols:
                for i in item[:2]:
                    if size.lower().endswith(i.lower()):
                        bytes = float(size[:-len(i)]) * item[2]
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            raise ValueError("can't parse " + size)
    else:
        TypeError('must be int, float or str' + ', not ' + type(size).__name__)
    num = bytes
    symbol = 'B'
    for item in __capacity_symbols[to]:
        if bytes >= item[2]:
            num = float(bytes) / item[2]
            symbol = item[0]
            break
    return '{:.{precision}f} {}'.format(num, symbol, precision = precision)

humanizedpercentage = lambda n: '{:.{precision}f}%'.format(n, precision = 1)
humanizedpercentage2 = lambda n: '{:.{precision}%}'.format(n, precision = 1)
