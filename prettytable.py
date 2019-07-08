#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    'PrettyTable',
    'PrettyVTable',
]

import sys, os, collections, itertools
from utils import align_size
from utils import RingLooper
from utils import transposelist
from colored import colorize
from colored import ColoredSetting

_default_field_paint = {'set' : ( 'bold', )}

_default_palette_paints = ( { 'fgcolor' : 'green',          'set' : ( 'bold', ) },
                            { 'fgcolor' : 'yellow',         'set' : ( 'bold', ) },
                            { 'fgcolor' : 'blue',           'set' : ( 'bold', ) },
                            { 'fgcolor' : 'magenta',        'set' : ( 'bold', ) },
                            { 'fgcolor' : 'cyan',           'set' : ( 'bold', ) },
                            { 'fgcolor' : 'light green',    'set' : ( 'bold', ) },
                            { 'fgcolor' : 'light yellow',   'set' : ( 'bold', ) },
                            { 'fgcolor' : 'light blue',     'set' : ( 'bold', ) },
                            { 'fgcolor' : 'light magenta',  'set' : ( 'bold', ) },
                            { 'fgcolor' : 'light cyan',     'set' : ( 'bold', ) }, )

class PrettyTable():
    def __init__(self,
        enable_painting = True,
        field_paint = None,
        palette_paints = None,
        padding_characters = '    ',
        align_boundary = 4):
        self.__enable_painting = enable_painting
        self.__field_paint = field_paint if field_paint != None else _default_field_paint
        self.__palette_paints = palette_paints if palette_paints != None else _default_palette_paints
        self.__padding_characters = padding_characters
        self.__align_boundary = align_boundary
        self.__fields = []
        self.__field_alignments = []
        self.__fixed_width_of_fields = []
        self.__records = []
        self.__max_size_of_columns = []

    def add_field(self, name, alignment = '<', fixed_width = None):
        self.__fields.append(name)
        if alignment not in '<^>':
            raise ValueError("alignment must be one of '<', '>' and '^'")
        self.__field_alignments.append(alignment)
        self.__fixed_width_of_fields.append(fixed_width)
        self.__max_size_of_columns.append(len(name))

    def add_record(self, *record):
        if len(record) != len(self.__fields):
            raise ValueError('record and fields must have the same length')
        record = list(map(str, record))
        self.__records.append(record)
        self.__max_size_of_columns = [ max(len(_), __) for _, __ in zip(record, self.__max_size_of_columns) ]

    def to_string(self):
        aligned_width_of_columns = map(lambda x: align_size(x, self.__align_boundary), self.__max_size_of_columns)
        aligned_width_of_columns = [ i if j == None else j for i, j in zip(aligned_width_of_columns, self.__fixed_width_of_fields) ]
        fmtstr = self.__padding_characters.join(['{:%s%d}' % (_, __) for _, __ in zip(self.__field_alignments, aligned_width_of_columns)])
        string = colorize(fmtstr.format(*self.__fields), enabling = self.__enable_painting, **self.__field_paint)
        string += os.linesep
        paletteiter = iter(RingLooper(*self.__palette_paints))
        for r in self.__records:
            string += colorize(fmtstr.format(*r), enabling = self.__enable_painting, **next(paletteiter))
            string += os.linesep
        return string

    def __str__(self):
        return self.to_string()

class PrettyVTable():
    def __init__(self,
        enable_painting = True,
        palette_paints = None,
        padding_characters = '    ',
        align_boundary = 4):
        self.__enable_painting = enable_painting
        self.__palette_paints = palette_paints if palette_paints != None else _default_palette_paints
        self.__padding_characters = padding_characters
        self.__align_boundary = align_boundary
        self.__fields = []
        self.__groups = []
        self.__column_alignments = []
        self.__fixed_width_of_columns = []
        self.__max_size_of_columns = []
        self.__column_cycler = None

    def add_column(self, alignment = '<', fixed_width = None):
        if alignment not in '<^>':
            raise ValueError("alignment must be one of '<', '>' and '^'")
        self.__column_alignments.append(alignment)
        self.__fixed_width_of_columns.append(fixed_width)
        self.__max_size_of_columns.append(0)

    def __make_default_columns(self, num, alignment = '<', fixed_width = None):
        for i in range(num):
            self.add_column(alignment, fixed_width)

    def add_field(self, name):
        if not self.__column_alignments:
            self.__make_default_columns(2)
        elif len(self.__column_alignments) < 2:
            raise ValueError('must be at least two columns')
        self.__fields.append(name)
        self.__max_size_of_columns[0] = max(len(name), self.__max_size_of_columns[0])

    def add_record(self, *record):
        if len(record) != len(self.__fields):
            raise ValueError('record and fields must have the same length')
        record = list(map(str, record))
        number_of_columns = len(self.__column_alignments)
        if self.__column_cycler is None:
            self.__column_cycler = itertools.cycle(range(1, number_of_columns))
        columnidx = next(self.__column_cycler)
        if columnidx == 1:
            empty_records_for_fill = [[''] * len(self.__fields)] * (number_of_columns - 2)
            self.__groups.append([self.__fields, record, *empty_records_for_fill])
        else:
            self.__groups[-1][columnidx] = record
        self.__max_size_of_columns[columnidx] = max(*map(len, record), self.__max_size_of_columns[columnidx])

    def to_string(self):
        aligned_width_of_columns = map(lambda x: align_size(x, self.__align_boundary), self.__max_size_of_columns)
        if self.__fixed_width_of_columns != None:
            aligned_width_of_columns = [ i if j == None else j for i, j in zip(aligned_width_of_columns, self.__fixed_width_of_columns) ]
        fmtstr = self.__padding_characters.join(['{:%s%d}' % (_, __) for _, __ in zip(self.__column_alignments, aligned_width_of_columns)])
        string = ''
        paletteiter = iter(RingLooper(*self.__palette_paints))
        for group in self.__groups:
            group = transposelist(group)
            paint = next(paletteiter)
            for row in group:
                string += colorize(fmtstr.format(*row), enabling = self.__enable_painting, **paint)
                string += os.linesep
        return string

    def __str__(self):
        return self.to_string()

def main(argv = None):
    if argv is None:
        argv = sys.argv
    pt = PrettyTable(enable_painting = True if sys.stdout.isatty() else False)
    pt.add_field('Name', alignment = '>')
    pt.add_field('Age', alignment = '<')
    pt.add_field('Birth', alignment = '>')
    pt.add_field('City', alignment = '<')
    pt.add_record('Zhang', '30', '1900', 'Shanghai')
    pt.add_record('Wang', '31', '1901', 'Beijing')
    pt.add_record('Li', '32', '1902', 'Shanghai')
    pt.add_record('Zhao', '33', '1903', 'Shanghai')
    pt.add_record('Song', '34', '1904', 'Beijing')
    pt.add_record('liu', '35', '1905', 'Guangdong')
    pt.add_record('Jack', '36', '1906', 'American')
    print(pt)

    print('1 ----------------------------------------------------')
    pt = PrettyTable(enable_painting = True if sys.stdout.isatty() else False)
    pt.add_field('Name', alignment = '>')
    pt.add_field('Age', alignment = '<')
    pt.add_field('Birth', alignment = '>')
    pt.add_field('City', alignment = '<')
    print(pt)

    print('2 ----------------------------------------------------')
    pt = PrettyTable(enable_painting = True if sys.stdout.isatty() else False, padding_characters = '  |  ')
    pt.add_field('Name', alignment = '>', fixed_width = 19)
    pt.add_field('Age', alignment = '<', fixed_width = 20)
    pt.add_field('Birth', alignment = '>', fixed_width = 20)
    pt.add_field('City', alignment = '<', fixed_width = 20)
    pt.add_record('Zhang', '30', '1900', 'Shanghai')
    pt.add_record('Wang', '31', '1901', 'Beijing')
    pt.add_record('Li', '32', '1902', 'Shanghai')
    pt.add_record('Zhao', '33', '1903', 'Shanghai')
    pt.add_record('Song', '34', '1904', 'Beijing')
    pt.add_record('liu', '35', '1905', 'Guangdong')
    pt.add_record('Jack', '36', '1906', 'American')
    print(pt)

    print('3 ----------------------------------------------------')
    pt = PrettyVTable(enable_painting = True if sys.stdout.isatty() else False)
    pt.add_column('<')
    pt.add_column('>')
    pt.add_column('>')
    pt.add_column('>')
    pt.add_column('<')
    pt.add_column('<')
    pt.add_column('<')
    pt.add_column('<')
    pt.add_column('<')
    pt.add_column('<')
    pt.add_column('<')
    pt.add_field('Name:')
    pt.add_field('Age:')
    pt.add_field('Birth:')
    pt.add_field('City:')
    pt.add_record('Zhang', '30', '1900', 'Shanghai')
    pt.add_record('Wang', '31', '1901', 'Beijing')
    pt.add_record('Li', '32', '1902', 'Shanghai')
    pt.add_record('Zhao', '33', '1903', 'Shanghai')
    pt.add_record('Song', '34', '1904', 'Beijing')
    pt.add_record('liu', '35', '1905', 'Guangdong')
    pt.add_record('Jack', '36', '1906', 'American')
    pt.add_record('Jack2', '36', '1906', 'American')
    pt.add_record('Jack3', '36', '1906', 'American')
    pt.add_record('Jack4', '36', '1906', 'American')
    pt.add_record('Jack5', '36', '1906', 'American')
    print(pt)

    print('4 ----------------------------------------------------')
    pt = PrettyVTable(enable_painting = True if sys.stdout.isatty() else False)
    pt.add_column(alignment = '>', fixed_width = 3)
    pt.add_column(alignment = '>', fixed_width = 3)
    pt.add_field('Name:')
    pt.add_field('Age:')
    pt.add_field('Birth:')
    pt.add_field('City:')
    pt.add_record('Zhang', '30', '1900', 'Shanghai')
    pt.add_record('Wang', '31', '1901', 'Beijing')
    pt.add_record('Li', '32', '1902', 'Shanghai')
    pt.add_record('Zhao', '33', '1903', 'Shanghai')
    pt.add_record('Song', '34', '1904', 'Beijing')
    pt.add_record('liu', '35', '1905', 'Guangdong')
    pt.add_record('Jack', '36', '1906', 'American')
    print(pt)

    print('5 ----------------------------------------------------')
    pt = PrettyVTable(enable_painting = True if sys.stdout.isatty() else False)
    pt.add_column()
    pt.add_column()
    pt.add_field('Name:')
    pt.add_field('Age:')
    pt.add_record('1', 'aa')
    pt.add_record('2', 'aa')
    pt.add_record('3', 'aa')
    pt.add_record('4', 'aa')
    pt.add_record('5', 'aa')
    pt.add_record('6', 'aa')
    pt.add_record('7', 'aa')
    pt.add_record('8', 'aa')
    pt.add_record('9', 'aa')
    pt.add_record('10', 'aa')
    pt.add_record('11', 'aa')
    pt.add_record('12', 'aa')
    print(pt)

    print('6 ----------------------------------------------------')
    pt = PrettyVTable(enable_painting = True if sys.stdout.isatty() else False, padding_characters = '  |  ')
    pt.add_column()
    pt.add_column()
    pt.add_field('Name:')
    pt.add_field('Age:')
    pt.add_field('Birth:')
    pt.add_field('City:')
    pt.add_record('Zhang', '30', '1900', 'Shanghai')
    pt.add_record('Wang', '31', '1901', 'Beijing')
    pt.add_record('Li', '32', '1902', 'Shanghai')
    pt.add_record('Zhao', '33', '1903', 'Shanghai')
    pt.add_record('Song', '34', '1904', 'Beijing')
    pt.add_record('liu', '35', '1905', 'Guangdong')
    pt.add_record('Jack', '36', '1906', 'American')
    print(pt)

if __name__ == '__main__':
    sys.exit(main())
