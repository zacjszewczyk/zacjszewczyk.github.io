#!/usr/bin/python

# Imports
from shutil import rmtree, copytree, copy # For directory and file operations
from os import mkdir # To create directories
from os.path import isdir # To check for directories
from sys import argv, stdout, exit # Enable writing multiple times to the same line
from colors import c # For output styling

# Target directory for public deployment
dst = "../Public/FirstCrack/"

# Method: CopyToDeploy
# Purpose: Copy the required files and folders to the deployment directory.
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def CopyToDeploy(v=False):
    # Clear the "system/*" tree in the deployment folder
    if (v): stdout.write(c.OKGREEN+"Clearing "+c.ENDC+"'"+dst+"system'"+c.OKGREEN+" ... "+c.ENDC)
    rmtree(dst+"system", ignore_errors=True)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"system'"+c.OKGREEN+" ... "+c.ENDC)
    # Copy the "./system" tree to the deployment folder
    copytree("./system", dst+"system")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"colors.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./colors.py", dst+"colors.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"ModTimes.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./ModTimes.py", dst+"ModTimes.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"Hash.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./Hash.py", dst+"Hash.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "Content" directory in the deployment folder
    if (not isdir(dst+"Content")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"Content'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"Content")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "local" directory in the deployment folder
    if (not isdir(dst+"local")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"local'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"local")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "local/assets" directory in the deployment folder
    if (not isdir(dst+"/local/assets")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"local/assets'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"local/assets")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the CSS file to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"local/assets/main.css'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./local/assets/main.css", dst+"local/assets/main.css")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

# Method: SanitizeDeploy
# Purpose: Sanitize FirstCrack files before deploying them publcily.
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def SanitizeDeploy(v=False):
    # Sanitize blog.py
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"blog.py'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"blog.py", "w").close()
    with open("./blog.py", "r") as source_fd, open(dst+"blog.py", "a") as dst_fd:
        for line in source_fd:
            if (line[0:8] == "base_url"):
                line = line.replace("https://zacs.site", "YOUR BASE URL HERE")
            if (line[0:6] == "byline"):
                line = line.replace("Zac J. Szewczyk", "YOUR NAME HERE")
            if (line[0:21] == "    BuildFromTemplate"):
                temp = line.split('", ')
                temp.pop(3)
                temp.insert(3,'description="DESCRIPTION HERE')
                line = '", '.join(temp)
            dst_fd.write(line)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    # Sanitize Markdown.py
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"Markdown.py'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"Markdown.py", "w").close()
    with open("./Markdown.py", "r") as source_fd, open(dst+"Markdown.py", "a") as dst_fd:
        for line in source_fd:

            dst_fd.write(line)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Sanitize system/404.html
    # Sanitize system/index.html
    # Sanitize system/projects.html
    # Sanitize system/template.htm
    pass

# Method: GenExFiles
# Purpose: Create example files in the deployment directory
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def GenExFiles(v=False):
    # Generate example content file
    pass

# If run as as a standalone program ...
if (__name__ == "__main__"):
    # Detect if running in verbose mode
    if ("-v" in argv):
        verbose = True
    else:
        verbose = False

    # Copy files to the deployment directory
    CopyToDeploy(verbose)
    SanitizeDeploy(verbose)
    GenExFiles(verbose)