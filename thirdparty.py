#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'chardet',
    'trydecodingbytes',
]

def chardet(bs):
    try:
        import chardet
        return chardet.detect(bs)
    except ImportError:
        try:
            import cchardet
            return cchardet.detect(bs)
        except ImportError:
            raise

def trydecodingbytes(bs):
    try:
        import bs4
        dammit = bs4.UnicodeDammit(bs)
        unicode_markup, original_encoding, tried_encodings = dammit.unicode_markup, dammit.original_encoding, dammit.tried_encodings
    except ImportError:
        unicode_markup, original_encoding, tried_encodings = None, None, None
    if unicode_markup:
        return unicode_markup, original_encoding
    try:
        encoding = chardet(bs)['encoding']
    except ImportError:
        encoding = None
    if not encoding:
        if tried_encodings and tried_encodings[0] and tried_encodings[0][0]:
            encoding = tried_encodings[0][0]
        else:
            encoding = 'utf-8'  # Guess
    try:
        s = bs.decode(encoding = encoding)
    except UnicodeDecodeError:
        s = str(bs)
        encoding = None
    return s, encoding
