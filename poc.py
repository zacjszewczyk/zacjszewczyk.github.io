#!/usr/bin/python

from os import listdir
from os.path import isfile

import sys

from os import stat, utime
def ModTimes(f1,f2):
    f1_mtime = stat(f1).st_mtime
    f2_mtime = stat(f2).st_mtime

    if (int(f1_mtime) == int(f2_mtime)):
        return True
    return False

for file in listdir("./stage"):
    # Ignore everything but HTML files
    if not (file[-4:] == "html" or file[-3:] == "xml" or file[-2:] == "js"):
        continue

    # Ignore files that have already been deployed
    if (isfile("./deploy/"+file) and ModTimes("./stage/"+file, "./deploy/"+file)):
        continue

    print "File needs updating:",file
    # utime("./deploy/"+file, (stat("./stage/"+file).st_mtime, stat("./stage/"+file).st_mtime))