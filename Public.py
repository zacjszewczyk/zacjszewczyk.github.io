#!/usr/bin/python

# Imports
from shutil import rmtree, copytree, copy # For directory and file operations
from os import mkdir # To create directories
from os.path import isdir # To check for directories
from sys import argv, stdout, exit # Enable writing multiple times to the same line
from colors import c # For output styling

# Target directory for public deployment
dst = "../Public/FirstCrack/"

if (__name__ == "__main__"):
    # Detect if running in verbose mode
    if ("-v" in argv):
        verbose = True
    else:
        verbose = False

    # Clear the "system/*" tree in the deployment folder
    if (verbose): stdout.write(c.OKGREEN+"Clearing "+c.ENDC+"'"+dst+"system'"+c.OKGREEN+" ... "+c.ENDC)
    rmtree(dst+"system", ignore_errors=True)
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"system'"+c.OKGREEN+" ... "+c.ENDC)
    # Copy the "./system" tree to the deployment folder
    copytree("./system", dst+"system")
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy "blog.py" and its dependencies to the deployment folder
    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"blog.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./blog.py", dst+"blog.py")
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"Markdown.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./Markdown.py", dst+"Markdown.py")
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"colors.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./colors.py", dst+"colors.py")
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"ModTimes.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./ModTimes.py", dst+"ModTimes.py")
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"Hash.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./Hash.py", dst+"Hash.py")
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "Content" directory in the deployment folder
    if (not isdir(dst+"Content")):
        if (verbose): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"Content'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"Content")
        if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "local" directory in the deployment folder
    if (not isdir(dst+"local")):
        if (verbose): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"local'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"local")
        if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "local/assets" directory in the deployment folder
    if (not isdir(dst+"/local/assets")):
        if (verbose): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"local/assets'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"local/assets")
        if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the CSS file to the deployment folder
    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"local/assets/main.css'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./local/assets/main.css", dst+"local/assets/main.css")
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)