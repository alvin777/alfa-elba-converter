#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs
import pprint

# import sys
# import os

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# print os.environ["PYTHONIOENCODING"]

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class CustomPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


# reader = UnicodeReader(open('Выписка_CSV по счету 40802840032280000017 с 01.01.2015 по 31.03.2015.csv', 'rb'), encoding='cp1251', delimiter='\t')
reader = UnicodeReader(open('Выписка_CSV по счету 40802840732280000016 с 01.01.2015 по 31.03.2015.csv', 'rb'), encoding='cp1251', delimiter='\t')
headers = reader.next()[:-1]
headers_ru = reader.next()[:-1]

# CustomPrinter().pprint(headers)
# CustomPrinter().pprint(headers_ru)

items = []

for line in reader:
    newItem = dict(zip(headers, line))
    if (u'курсовая разница' in newItem['text70']):
        continue
    # print CustomPrinter().pprint(zip(headers, line))
    # CustomPrinter().pprint(newItem)
    print newItem['oper']
    items.append(newItem)


from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader('./', encoding='cp1251')
env = Environment(loader=loader)

template = env.get_template('1c_template.txt')

with codecs.open('1c.txt', 'w', 'cp1251') as file:
    file.write(template.render(account=items[0], itemsList=items))
