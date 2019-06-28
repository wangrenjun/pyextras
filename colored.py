#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'init_colored',
    'Colored',
    'AnsiColored',
    'colorize',
    'ttyautocolorize',
    'combine',
    'EscapeSet',
    'EscapeReset',
    'EscapeFgColor',
    'EscapeBgColor',
]

import sys, enum, abc, collections
from utils import joiniterable
from utils import streamistty

_has_enabled_coloring = True

def init_colored(on = True):
    global _has_enabled_coloring
    if not isinstance(on, bool):
        raise TypeError('must be bool' + ', not ' + type(on).__name__)
    on, _has_enabled_coloring = _has_enabled_coloring, on
    return on

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

class Colored(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def __add__(self, other):
        pass
    @abc.abstractmethod
    def __radd__(self, other):
        pass
    @abc.abstractmethod
    def __str__(self):
        pass
    @abc.abstractmethod
    def __repr__(self):
        pass

class AnsiColored(Colored):
    def __init__(self, *args, enabling = True, **style):
        string = ' '.join(args)
        if _has_enabled_coloring is True and enabling is True:
            paint = combine(**style)
            if paint:
                string = paint + string + EscapeReset.NORMAL.value
        self.__string = string

    def __add__(self, other):
        if isinstance(other, (self.__class__, str)):
            return self.__class__(self.__string + str(other))
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (self.__class__, str)):
            return self.__class__(str(other) + self.__string)
        else:
            return NotImplemented

    def __str__(self):
        return self.__string

    def __repr__(self):
        return "%s.%s(%r)" % (self.__class__.__module__,
                              self.__class__.__qualname__,
                              self.__dict__)

def colorize(*args, enabling = None, **style):
    return AnsiColored(*args, enabling = enabling, **style)

def ttyautocolorize(stream, *args, **style):
    return AnsiColored(*args, enabling = streamistty(stream), **style)

def combine(**style):
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

EscapeSet = enum.Enum('EscapeSet', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _sets.items() })
EscapeReset = enum.Enum('EscapeReset', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _resets.items() })
EscapeFgColor = enum.Enum('EscapeFgColor', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _fgcolors.items() })
EscapeBgColor = enum.Enum('EscapeBgColor', { '_'.join(k.upper().split(' ')): _esc(v) for k, v in _bgcolors.items() })

def main(argv = None):
    if argv is None:
        argv = sys.argv

    assert init_colored(False) == True
    assert init_colored(True) == False
    assert _has_enabled_coloring == True

    c1 = AnsiColored('1.', 'hello', 'world', '你好', fgcolor = 'red', bgcolor = 'grey')
    print(c1)

    c2 = AnsiColored('2.', 'hello', 'world', '你好', fgcolor = 'black', bgcolor = 'cyan', set = [ 'bold', 'crossed out' ])
    print(c2)
    print(c1 + c2)
    print(c2 + '世界')
    print('世界' + c2)
    assert str(c2) == _esc([30, 46, 1, 9]) + '2. hello world 你好' + _esc(0)

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
        print(AnsiColored(l, **next(paletteiter)))

if __name__ == "__main__":
    sys.exit(main())
