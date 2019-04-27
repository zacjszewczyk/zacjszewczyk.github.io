#!/usr/bin/python

# Imports
from colors import c # Style output
from shutil import copy, copystat

# Method: CopyFile
# Purpose: Copy an existing file, and optionally preserve metadata
# Parameters: 
# - tgt: Path to source file. (String)
# - dst: Path to destination file. (String)
# - metadata: True to retain metadata, False to discard. (Bool)
# - verbose: True for output, False for silent. (Bool)
# Return: 0 for success, 1 for error. (Int)
def CopyFile(tgt,dst,metadata=True,verbose=False):
    from sys import stdout # Enable writing multiple times to the same line
    from os.path import isfile # File checking

    # Ensure source file exists. Print error message and exit if not.
    if (not isfile(tgt)):
        if (verbose): stdout.write(c.FAIL+"Target file does not exist."+c.ENDC+"\n")
        return 1

    # Copy source to destination
    if (verbose): stdout.write(c.OKGREEN+"Copying "+c.ENDC+tgt+" -> "+dst+" ...")
    try: 
        copy(tgt, dst)
        if (verbose): stdout.write(c.OKGREEN+" done."+c.ENDC+"\n")
    except:
        stdout.write(c.FAIL+"Error copying."+c.ENDC+"\n")
        return 1

    # Optionally, copy metadata from source to destination
    if (metadata):
        if (verbose): stdout.write(c.OKGREEN+"Metadata "+c.ENDC+tgt+" -> "+dst+" ...")
        try:
            copystat(tgt, dst)
            if (verbose): stdout.write(c.OKGREEN+" done."+c.ENDC+"\n")
        except:
            stdout.write(c.FAIL+"Error."+c.ENDC+"\n")
            return 1

    # Return 0 on success
    return 0

# Enable standalone functionality
if (__name__ == "__main__"):
    # Imports
    from sys import argv, exit # Command line parameters and exiting on error
    
    # Basic bounds checking
    if (len(argv) < 3):
        print c.FAIL+"Invalid parameters."+c.ENDC
        exit(1)

    # Detect if running in verbose mode, and run the copy command accordingly.
    if ("-v" in argv):
        argv.remove("-v")
        CopyFile(argv[1],argv[2],verbose=True)
    else:
        CopyFile(argv[1],argv[2])