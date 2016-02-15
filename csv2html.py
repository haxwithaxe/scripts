#!/usr/bin/env python2
""" Very simplistic csv to html table converter """


__authors__ = ['haxwithaxe <me@haxwithaxe.net>']
__license__ = 'GPLv3'


import csv


def attrib_to_string(**attribs):
    if not attribs:
        return ''
    return ' '.join(['%s="%s"' % (key,value) for key,value in attribs])


def xml_elem(*strings, **attribs):
    return '<%s %s>%s</%s>' % (elem, attrib_to_string(**attribs) , ''.join(strings), elem)


def td(*strings, **attribs):
    attribs['elem'] = 'td'
    return xml_elem(*strings, **attribs)


def th(*strings, **attribs):
    attribs['elem'] = 'th'
    return xml_elem(*strings, **attribs)


def tr(*strings, **attribs):
    attribs['elem'] = 'tr'
    return xml_elem(*strings, **attribs)


def table(*string, **attribs):
    attribs['elem'] = 'table'
    return xml_elem(*string, **attribs)


def load_csv(filename):
    with open(filename, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)


def make_header(reader):
    headers = []
    for f in reader.fieldnames:
        headers.append(th(f))
    return tr(*headers)


def make_contents(reader):
    body = []
    line = True
    while line:
        row = []
        line = reader.next()
        if line:
            for i in line:
                row.append(td(i))
            body.append(tr(row))
    return body


def make_table(reader):
    header = make_header(reader)
    body = make_contents(reader)
    header += body
    return table(header*)


def make_page(reader):
    t = make_table(reader)
    return xml_elem(xml_elem(t, elem='body'), 'html')
    

