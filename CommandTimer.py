#!/usr/bin/env python

import timeit as t

#print "os.path.getmtime:\t",t.timeit("os.path.getmtime('test.sh')","import os",number=10000)
#print "os.stat:\t\t",t.timeit("os.stat('test.sh').st_mtime","import os", number=10000)

import os
import time

#print "vars:\t\t",t.timeit("print '%d/%d/%d/%d:%d:%d' % (t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)","import time; import os; t = time.localtime(os.stat('test.sh').st_mtime)",number=10000)
#print "vars:\t\t",t.timeit("print time.strftime('%Y/%m/%d/%H:%M:%S', t)","import time; import os; t = time.localtime(os.stat('test.sh').st_mtime)",number=10000)

#print "replace:\t\t",t.timeit("string.replace('things','nothing')","string = 'Temp string with some things in it.'",number=10000)
#print "re.sub:\t\t",t.timeit("re.sub('things','nothing',string)","import re; string = 'Temp string with some things in it.'",number=10000)

print "endswith:\t",t.timeit("each.endswith('.txt')","each = 'Were Live.txt'", number=10000)
print "in:\t\t",t.timeit("'.txt' in each","each = 'Were Live.txt'", number=10000)
print "index:\t\t",t.timeit("'txt' == each[-3:]","each = 'Were Live.txt'", number=10000)

# print "endswith:\t",t.timeit("each.startswith('http')","each = 'http://Were Live.txt'", number=10000)
# print "index:\t\t",t.timeit("'http' == each[0:4]","each = 'http://Were Live.txt'", number=10000)

# print "string.lower():\t",t.timeit("each.lower()","each='Conjecture Regarding Larger iPhone Displays.txt'", number=10000)
# func = """\
# import string
# letter_set = frozenset(string.ascii_lowercase + string.ascii_uppercase)
# tab = string.maketrans(string.ascii_lowercase + string.ascii_uppercase,string.ascii_lowercase * 2)
# deletions = ''.join(ch for ch in map(chr,range(256)) if ch not in letter_set)
# each='Conjecture Regarding Larger iPhone Displays.txt'
# def makelower(s):
#     return string.translate(s, tab, deletions)"""
# to_exec = "makelower(each)"
# print "translate:\t",t.timeit(stmt=to_exec,setup=func, number=10000)

# environment = """\
# from sys import modules
# from sys import stdout
# """
# to_exec = "from sys import stdout"
# print "duplicate:\t",t.timeit(stmt=to_exec,setup=environment, number=10000)
# environment = """\
# from sys import modules
# """
# to_exec = """\
# if ("stdout" not in modules.keys()):
#     from sys import modules
# """
# print "check:\t\t",t.timeit(stmt=to_exec,setup=environment, number=10000)