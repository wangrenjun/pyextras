#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'exitcode',
    'signame_to_signo',
    'signo_to_signame',
    'set_trap_handler',
]

import sys, signal, enum
from colored import colorize
from utils import streamistty

class exitcode(enum.IntEnum):
    EC_OK = 0                   # Successful termination
    EC_ERROR = 1                # General errors
    EC_USAGE_ERROR = 2          # Usage error
    EC_ENOENT = 97              # No such file or directory
    EC_INVAL = 98               # Invalid argument
    EC_ASSERT_FAILED = 99
    EC_ILLEGAL_CMD = 127        # Command not found
    EC_FATAL_SIGNAL_BASE = 128  # Base value for fatal error signal "n"
    EC_CONTRL_C = 130           # Script terminated by Control-C(128 + 2)

_siglist = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items())) if v.startswith('SIG') and not v.startswith('SIG_'))

def signame_to_signo(sname):
    return int(getattr(signal, sname, 0))

def signo_to_signame(sno):
    return _siglist.get(sno)

def _on_trapped(signo, frame):
    print(str(colorize('Interrupted by %s' % (signo_to_signame(signo)), enabling = streamistty(sys.stderr), fgcolor = 'green', set = ( 'bold', ))), file = sys.stderr)
    sys.exit(exitcode.EC_FATAL_SIGNAL_BASE + signo)

def set_trap_handler(sigs, handler = None):
    if handler and not callable(handler):
        raise TypeError("'" + type(handler).__name__ + "'" + ' object is not callable')
    for _ in sigs:
        signal.signal(_, handler or _on_trapped)

def main(argv = None):
    if argv is None:
        argv = sys.argv
    set_trap_handler((signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM))
    import time
    time.sleep(9999)

if __name__ == '__main__':
    sys.exit(main())
