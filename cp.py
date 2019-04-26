#!/usr/bin/python

# Method: CopyFile
# Purpose: Copy an existing file, and optionally preserve metadata
# Parameters: 
# - tgt: Path to source file. (String)
# - dst: Path to destination file. (String)
# - metadata: True to retain metadata, False to discard. (Bool)
# - verbose: True for output, False for silent. (Bool)
# Return: 0 for success, 1 for error. (Int)
def CopyFile(tgt,dst,metadata=True,verbose=False):
    from sys import stdout
    from os.path import isfile
    from colors import c

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

if (__name__ == "__main__"):
    CopyFile("blah","blah",verbose=True)