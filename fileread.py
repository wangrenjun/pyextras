#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'FileRead',
]

import os, sys

class FileRead:
    def __init__(self,
        files = None,
        mode = 'r',
        prompt_when_stdin = None,
        openhook = None,
        readhook = None):
        if isinstance(files, str):
            files = (files, )
        elif isinstance(files, os.PathLike):
            files = (os.fspath(files), )
        else:
            if not files:
                files = ('-', )
            else:
                files = tuple(files)
        self.__files = files
        self.__filename = None
        self.__isstdin = False
        if mode not in ('r', 'rb', 'rt'):
            raise ValueError("FileRead opening mode must be one of 'r', 'rb' and 'rt'")
        self.__mode = mode
        self.__prompt_when_stdin = prompt_when_stdin
        self.__openhook = openhook or FileRead.hook_open()
        self.__readhook = readhook or (lambda f: f.read())

    def __read(self):
        for self.__filename in self.__files:
            self.__isstdin = False
            if self.__filename == '-':
                self.__filename = sys.stdin.name    # '<stdin>'
                self.__isstdin = True
                if self.__prompt_when_stdin:
                    print(self.__prompt_when_stdin, flush = True)
                if 'b' in self.__mode:
                    content = self.__readhook(getattr(sys.stdin, 'buffer', sys.stdin))
                else:
                    content = self.__readhook(sys.stdin)
            else:
                content = self.__readhook(self.__openhook(self.__filename, self.__mode))
            yield content

    def __iter__(self):
        return self.__read()

    def isstdin(self):
        return self.__isstdin

    def filename(self):
        return self.__filename

    @classmethod
    def hook_open(cls, encoding = None, errors = None, newline = None):
        return lambda f, m: open(f, mode = m, encoding = encoding, errors = errors, newline = newline)

def main(argv = None):
    if argv is None:
        argv = sys.argv

    fl = FileRead(prompt_when_stdin = 'Press Ctrl-D when finished')
    try:
        for cont in fl:
            print(fl.filename(), fl.isstdin(), '---------------------------------------------------------------------')
            print(cont)
    except OSError as e:
        print(str(e))

    files = ( '-', '/home/wangrj/a.php', '/home/wangrj/a.sh', '/home/wangrj/b.sh' )
    fl = FileRead(files, prompt_when_stdin = 'Press Ctrl-D when finished')
    try:
        for cont in fl:
            print(fl.filename(), fl.isstdin(), '---------------------------------------------------------------------')
            print(cont)
    except OSError as e:
        print(str(e))

    files = ( '-', '/home/wangrj/a.php', '/home/wangrj/a.sh', '/home/wangrj/not_exist', '/home/wangrj/b.sh' )
    fl = FileRead(files)
    try:
        for cont in fl:
            print(fl.filename(), fl.isstdin(), '---------------------------------------------------------------------')
            print(cont)
    except OSError as e:
        print(str(e))

    files = ( '/home/wangrj/bbb' )
    fl = FileRead(files)
    try:
        for cont in fl:
            print(fl.filename(), fl.isstdin(), '---------------------------------------------------------------------')
            print(type(cont), len(cont))
    except OSError as e:
        print(str(e))

    files = ( '/home/wangrj/bbb' )
    fl = FileRead(files, mode = 'rb')
    try:
        for cont in fl:
            print(fl.filename(), fl.isstdin(), '---------------------------------------------------------------------')
            print(type(cont), len(cont))
    except OSError as e:
        print(str(e))

    files = '/home/wangrj/zh.txt'
    def myopen(f, m, encoding, errors):
        print('myopen, filename: %s, mode: %s, encoding: %s, errors: %s' % (f, m, encoding, errors))
        return open(f, mode = m, encoding = encoding, errors = errors)

    def custom_open(encoding = None, errors = None):
        return lambda f, m: myopen(f, m, encoding, errors)

    fl = FileRead(files, openhook = custom_open(encoding = 'gb2312'))
    try:
        for cont in fl:
            print(fl.filename(), fl.isstdin(), '---------------------------------------------------------------------')
            print(cont)
    except OSError as e:
        print(str(e))

if __name__ == "__main__":
    sys.exit(main())
