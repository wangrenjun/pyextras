#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'ColoredArgParser',
]

import sys, argparse
from colored import colorize
from colored import ColoredSetting

class ColoredArgParser(argparse.ArgumentParser):
    __styles = { 'usage' : { 'fgcolor' : 'yellow', 'set' : ( 'bold', ) },
                 'help' :  { 'fgcolor' : 'blue', 'set' : ( 'bold', ) },
                 'error' : { 'fgcolor' : 'red', 'set' : ( 'bold', ) }, }

    def __init__(self, **kwargs):
        styles = kwargs.pop('styles', None)
        super().__init__(**kwargs)
        if styles != None:
            self.__styles = styles

    def print_usage(self, file = sys.stdout):
        usage = self.format_usage()
        usage = usage[0].upper() + usage[1:]
        self._print_message(colorize(usage, enabling = ColoredSetting().is_colorize(file), **self.__styles['usage']), file)

    def print_help(self, file = sys.stdout):
        help = self.format_help()
        help = help[0].upper() + help[1:]
        self._print_message(colorize(help, enabling = ColoredSetting().is_colorize(file), **self.__styles['help']), file)

    def exit(self, status = 0, message = None):
        if message:
            self._print_message(colorize(message, enabling = ColoredSetting().is_colorize(sys.stderr), **self.__styles['error']), sys.stderr)
        sys.exit(status)

    def error(self, message):
        self.print_usage(sys.stderr)
        message = '%(prog)s: ERROR: %(message)s\n' % { 'prog': self.prog, 'message': message }
        self.exit(2, message)

    def print_error(self, message):
        message = '%(prog)s: ERROR: %(message)s\n' % { 'prog': self.prog, 'message': message }
        self._print_message(colorize(message, enabling = ColoredSetting().is_colorize(sys.stderr), **self.__styles['error']), sys.stderr)

def main(argv = None):
    if argv is None:
        argv = sys.argv
    ColoredSetting('never')
    cap = ColoredArgParser()
    cap.add_argument('-s', dest = 'simple_value', help = 'Simple value')
    cap.add_argument('-l', '--longoption', dest = 'longoption_value', help = 'Longoption value')
    results = cap.parse_args()
    print(results)
    cap.print_error('Just print error without terminate')
    #cap.exit(2, 'Manual abort\n')
    #cap.error('Manual error')

if __name__ == "__main__":
    sys.exit(main())
