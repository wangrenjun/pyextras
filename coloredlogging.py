#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'ColoredFormatter',
    'ColoredLogger',
    'init_colored_logger',
]

import sys, logging
from colored import colorize
from colored import ColoredSetting

_levelstyles = { 'INFO' :     { 'fgcolor' : 'green', 'set' : ( 'bold', ) },
                 'WARNING':   { 'fgcolor' : 'yellow', 'set' : ( 'bold', ) },
                 'ERROR' :    { 'fgcolor' : 'red', 'set' : ( 'bold', ) },
                 'CRITICAL' : { 'fgcolor' : 'light red', 'set' : ( 'bold', ) }, }

_default_format = '%(filename)s: %(levelname)s: %(message)s'
_default_dateformat = '%Y-%m-%d %H:%M:%S %p'

class ColoredFormatter(logging.Formatter):
    def __init__(self,
        fmt = None,
        datefmt = None,
        stream = sys.stderr):
        super().__init__(_default_format if fmt is None else fmt,
            _default_dateformat if datefmt is None else datefmt)
        self.__stream = stream

    def format(self, record):
        msg = super().format(record)
        return str(colorize(msg, enabling = ColoredSetting().is_colorize(self.__stream), **_levelstyles.get(record.levelname, {})))

class ColoredLogger(logging.Logger):
    def __init__(self, name, level = logging.NOTSET, stream = sys.stderr):
        super().__init__(name, level)
        self.__stream_handler = logging.StreamHandler(stream)
        self.__stream_handler.setFormatter(ColoredFormatter(stream = stream))
        self.addHandler(self.__stream_handler)

def init_colored_logger():
    logging.addLevelName(logging.DEBUG, 'DEBUG')
    logging.addLevelName(logging.INFO, 'INFO')
    logging.addLevelName(logging.WARNING, 'WARNING')
    logging.addLevelName(logging.ERROR, 'ERROR')
    logging.addLevelName(logging.CRITICAL, 'CRITICAL')
    logging.setLoggerClass(ColoredLogger)

def main(argv = None):
    if argv is None:
        argv = sys.argv
    init_colored_logger()
    ColoredSetting('always')

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log.debug("This is debug")
    log.info("This is info")
    log.warning("This is warning")
    log.error("This is error")
    log.critical("This is critical")
    print()

    log2 = logging.getLogger(__name__)
    log2.setLevel(logging.DEBUG)
    log2.debug("This is debug")
    log2.info("This is info")
    log2.warning("This is warning")
    log2.error("This is error")
    log2.critical("This is critical")
    print()

    log.debug("This is debug")
    log.info("This is info")
    log.warning("This is warning")
    log.error("This is error")
    log.critical("This is critical")

if __name__ == "__main__":
    sys.exit(main())
