#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'colorizeansi',
    'ttyautocolorizeansi',
    'combineansi',
    'colorize',
    'ttyautocolorize',
    'combine',
    'escapeset',
    'escapereset',
    'escapefgcolor',
    'escapebgcolor',
    'ColoredSetting',
]

import sys, enum, abc, collections
from utils import joiniterable
from utils import streamistty
from utils import joiniterable
from utils import Singleton

_sets = dict(zip(
        ( 'bold', 'dim', 'italic', 'underlined', 'blink', 'rapid blink', 'reverse', 'hidden', 'crossed out', ),
        ( str(_) for _ in range(1, 10))))
_resets = dict(zip(
        ( 'bold', 'dim', 'italic', 'underlined', 'blink', 'rapid blink', 'reverse', 'hidden', 'crossed out', ),
        ( str(_) for _ in range(21, 30))))
_resets.update({ 'normal' : '0', 'fg reset' : '39', 'bg reset' : '49', })
_fgcolors = dict(zip(
        ( 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'silver', ),
        ( str(_) for _ in range(30, 38))))
_fgcolors.update(dict(zip(
        ( 'grey', 'light red', 'light green', 'light yellow', 'light blue', 'light magenta', 'light cyan', 'white', ),
        ( str(_) for _ in range(90, 98)))))
_bgcolors = dict(zip(
        ( 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'silver', ),
        ( str(_) for _ in range(40, 48))))
_bgcolors.update(dict(zip(
        ( 'grey', 'light red', 'light green', 'light yellow', 'light blue', 'light magenta', 'light cyan', 'white', ),
        ( str(_) for _ in range(100, 108)))))

def _esc(codes):
    if isinstance(codes, (int, str)):
        return '\033[{}m'.format(codes)
    elif isinstance(codes, collections.Iterable):
        return '\033[{}m'.format(joiniterable(';', codes))
    else:
        raise TypeError('must be one of int, str, iterable' + ', not ' + type(codes).__name__)

def colorizeansi(*args, enabling = True, **style):
    argstring = joiniterable(' ', args)
    if enabling:
        paint = combineansi(**style)
        if paint:
            argstring = paint + argstring + escapereset.NORMAL.value
    return argstring

def ttyautocolorizeansi(stream, *args, **style):
    return colorizeansi(*args, enabling = streamistty(stream), **style)

def combineansi(**style):
    fields = {
        'set' :     lambda x: [ _sets[_] for _ in x ],
        'reset' :   lambda x: [ _resets[_] for _ in x ],
        'fgcolor' : lambda x: [ _fgcolors[x] ],
        'bgcolor' : lambda x: [ _bgcolors[x] ],
    }
    l = []
    for k, v in style.items():
        f = fields.get(k)
        if f:
            l.extend(f(v))
    return _esc(l) if l else ''

def colorize(*args, enabling = True, **style):
    return colorizeansi(*args, enabling = enabling, **style)

def ttyautocolorize(stream, *args, **style):
    return ttyautocolorizeansi(stream, *args, **style)

def combine(**style):
    return combineansi(**style)

escapeset = enum.Enum('escapeset', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _sets.items() })
escapereset = enum.Enum('escapereset', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _resets.items() })
escapefgcolor = enum.Enum('escapefgcolor', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _fgcolors.items() })
escapebgcolor = enum.Enum('escapebgcolor', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _bgcolors.items() })

class ColoredSetting(metaclass = Singleton):
    def __init__(self, when = 'auto', autocb = streamistty):
        if when == 'always':
            self.__has_enabled_colorize = True
        elif when == 'never':
            self.__has_enabled_colorize = False
        else:
            self.__has_enabled_colorize = autocb
    def is_colorize(self, stream):
        return self.__has_enabled_colorize if isinstance(self.__has_enabled_colorize, bool) else self.__has_enabled_colorize(stream)

def main(argv = None):
    if argv is None:
        argv = sys.argv

    c1 = colorize('1.', 'hello', 'world', '你好', fgcolor = 'red', bgcolor = 'grey')
    print(c1)

    c2 = colorize('2.', 'hello', 'world', '你好', fgcolor = 'black', bgcolor = 'cyan', set = [ 'bold', 'crossed out' ])
    print(c2)
    print(c1 + c2)
    print(c2 + '世界')
    print('世界' + c2)
    assert c2 == _esc([30, 46, 1, 9]) + '2. hello world 你好' + _esc(0)

    escseq = combine(fgcolor = 'green', bgcolor = 'silver', set = [ 'bold', 'underlined', 'blink' ])
    print(repr(escseq))
    assert len(escseq) == len(_esc([32, 47, 1, 4, 5]))

    palette_paints = ( { 'fgcolor' : 'red', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'green', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'yellow', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'blue', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'magenta', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'cyan', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'light red', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'light green', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'light yellow', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'light blue', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'light magenta', 'set' : ( 'bold', ) },
                       { 'fgcolor' : 'light cyan', 'set' : ( 'bold', ) }, )
    from utils import RingLooper
    paletteiter = iter(RingLooper(*palette_paints))
    from this import s
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i+c)] = chr((i+13) % 26 + c)
    for l in "".join([d.get(c, c) for c in s]).splitlines():
        print(colorize(l, **next(paletteiter)))

if __name__ == "__main__":
    sys.exit(main())
