#!/usr/bin/python

# Imports
from shutil import rmtree, copytree, copy # For directory and file operations
from os import mkdir # To create directories
from os.path import isdir # To check for directories

# Target directory for public deployment
dst = "../Public/FirstCrack/"

# Clear the "system/*" tree in the deployment folder
rmtree(dst+"system", ignore_errors=True)
# Copy the "./system" tree to the deployment folder
copytree("./system", dst+"system")

# Copy "blog.py" and its dependencies to the deployment folder
copy("./blog.py", dst+"blog.py")
copy("./Markdown.py", dst+"Markdown.py")
copy("./colors.py", dst+"colors.py")
copy("./ModTimes.py", dst+"ModTimes.py")
copy("./Hash.py", dst+"Hash.py")

# Create the "Content" directory in the deployment folder
if (not isdir(dst+"Content")):
    mkdir(dst+"Content")

# Create the "local" directory in the deployment folder
if (not isdir(dst+"local")):
    mkdir(dst+"local")
# Create the "local/assets" directory in the deployment folder
if (not isdir(dst+"/local/assets")):
    mkdir(dst+"/local/assets")

# Copy the CSS file to the deployment folder
copy("./local/assets/main.css", dst+"local/assets/main.css")