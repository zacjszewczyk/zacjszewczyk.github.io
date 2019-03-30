#!/usr/bin/python

# Import functions for CLI
from sys import argv, exit

# Method: Fetch
# Purpose: Download logs
# Parameters: none
def Fetch():
    # Import functions for file operations
    from os.path import isdir, isfile
    from os import mkdir
    
    # Make sure 'logs' directory exists
    if (not isdir("./logs")):
        mkdir("./logs")

    # Import functions for S3 session
    from boto3.session import Session
    import boto3

    # Private access key information
    ACCESS_KEY = 'AKIA4K7UTVOAUNQFLO7T'
    SECRET_KEY = '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'

    # Instantiate a new session
    session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3 = session.resource('s3')
    b = s3.Bucket('logs.zacs.site')

    # Iterate over each object in the bucket
    for file in b.objects.all():
        # If the file does not exist on the local machine, downlaod it
        if (not isfile("."+file.key)):
            print "Downloading '%s' to location '%s'" % (file.key, "."+file.key)
            b.download_file(file.key, "."+file.key)

# Method: Parse
# Purpose: Parse logs
# Parameters: none
def Parse():
    print "Parsing."

# Method: Push
# Purpose: Update site
# Parameters: none
def Push():
    print "Pushing."

if (__name__ == "__main__"):
    
    # Basic input checking
    if (len(argv) <= 1):
        print "Enter parameter."
        exit(1)
    if (len(argv) > 2):
        print "Too many parameters."
        exit(1)

    # Handle input
    ## Fetch logs
    if (argv[1] == "fetch"):
        Fetch()
    ## Parse logs
    elif (argv[1] == "parse"):
        Parse()
    elif (argv[1] == "push"):
        Push()
    ## Invalid parameter. Notify user and exit.
    else:
        print "Enter a valid parameter."
        exit(1)