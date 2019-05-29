#!/usr/bin/python

from shutil import rmtree, copytree, copy
from os import mkdir
from os.path import isdir

dst = "../Public/FirstCrack/"

rmtree(dst+"system", ignore_errors=True)
copytree("./system", dst+"system")

copy("./blog.py", dst+"blog.py")
copy("./Markdown.py", dst+"Markdown.py")
copy("./colors.py", dst+"colors.py")
copy("./ModTimes.py", dst+"ModTimes.py")
copy("./Hash.py", dst+"Hash.py")

if (not isdir(dst+"Content")):
    mkdir(dst+"Content")

if (not isdir(dst+"local")):
    mkdir(dst+"local")
if (not isdir(dst+"/local/assets")):
    mkdir(dst+"/local/assets")