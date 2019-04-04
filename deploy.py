#!/usr/bin/python

# Global imports
## Import functions for file operations
from os.path import isdir, isfile
from os import mkdir, listdir

# Amazon S3 Server Access Log Format
# https://docs.aws.amazon.com/AmazonS3/latest/dev/LogFormat.html

# Class: colors
# Purpose: provide easy access to ASCII escape codes for styling output
class colors():
    HEADER = '\033[95m' # Pink
    OKBLUE = '\033[94m' # Purple
    OKGREEN = '\033[92m' # Green
    WARNING = '\033[93m' # Yellow
    FAIL = '\033[91m' # Red
    ENDC = '\033[0m' # None
    BOLD = '\033[1m' # Blue
    UNDERLINE = '\033[4m' # Underline
# Instantiate the "colors" class, for output styling
c = colors()

# Method: AssociateGroups
# Purpose: Given an array of groups from Amazon S3 Server Access
# Log Format, return a dictionary with the field names as keys
# Parameters: 
# - groups: Groups from Amazon S3 Server Access Log Format
# Return: 
# - _dict: Dictionary of groups with the right label as their key (Dictionary)
def AssociateGroups(groups):
    _dict = {}
    _dict_labels = ["owner","bucket","timestamp","remote_ip","requester","request_id","operation","key","request_uri","http_status","error_code","bytes_sent","object_size","transmission_time","turnaround_time","referrer","user_agent","version_id","host_id","signature_version","cipher_suite","authentication_type","host_header","tls_version"]
    for _i, _field in enumerate(groups, start=0):
        if (_i < len(_dict_labels)):
            _dict[_dict_labels[_i]] = _field
        else:
            _dict[_i] = _field
    return _dict

# Method: CaptureGroups
# Purpose: Return array of groups from Amazon S3 Server Access Log Format
# Parameters: 
# - entry: Log in Amazon S3 Server Access Log Format
# Return: 
# - _capture_groups: Array of capture groups (Array)
def CaptureGroups(entry):
    _delimeters = ['"', '[', ']', ' ']
    _group = ""
    _closing_char = ' '
    _capture_groups = []
    for character in entry:
        if (_group == "" and _closing_char == ' ' and character in _delimeters):
            if (character == '['):
                _closing_char = ']'
            else:
                _closing_char = character
        elif (character == _closing_char):
            _capture_groups.append(_group)
            _group = ""
            _closing_char = ' '
        else:
            _group += character
    else:
        _capture_groups.append(_group.strip())
    return _capture_groups

# Method: CheckDirAndCreate
# Purpose: Check for the existence of a given directory, and create it if it
#          doesn't exist.
# Parameters:
# - tgt: Directory to test and maybe create
def CheckDirAndCreate(tgt, verbose=False):
    if (not isdir(tgt)):
        from sys import stdout
        if (verbose == True): stdout.write(c.OKGREEN+"Creating "+tgt+" ..."+c.ENDC)
        mkdir(tgt)
        if (verbose == True): stdout.write(c.OKGREEN+"Done.\n"+c.ENDC)

# Method: CreateTree
# Purpose: Check for the existence of a given directory tree, and create it
#          if it doesn't exist.
# Parameters:
# - tree: Directory tree to test and maybe create
def CreateTree(tree, verbose=False):
    from sys import stdout
    tree = tree.split("/")
    for folder in tree:
        if (folder == "."):
            continue
        d = "/".join(tree[:tree.index(folder)])+"/"+folder
        if (not isdir(d)):
            if (verbose == True): stdout.write(c.OKGREEN+"Creating "+d+" ..."+c.ENDC)
            mkdir(d)
            if (verbose == True): stdout.write(c.OKGREEN+"Done.\n"+c.ENDC)

# Method: Clear
# Purpose: Clear the target directory
# Parameters: 
# - tgt: Target directory to be cleared
# Return: none
def Clear(tgt):
    # Import methods for file operations
    from os import walk, remove
    from sys import stdout

    # Keep track of number of files deleted
    i = 0

    # Move through ./stage and all subdirectories
    for path, subdirs, files in walk(tgt):
        # Remove .DS_Store from file list
        if (".DS_Store" in files):
            files.remove(".DS_Store")

        # If there are no files to remove in the directory, warn
        # the user.
        if (len(files) == 0):
            print "%sNothing to clear in %s%s" % (c.WARNING, path, c.ENDC)
            continue

        # Delete all non-hidden files in tgt/*
        for name in files:
            # Ignore hidden files
            if (name[0] == '.'):
                continue
            stdout.write(c.FAIL+"Removing file at: "+c.ENDC+path+"/"+name+" ...")
            remove(path+"/"+name)
            stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
            i += 1
    
    print c.WARNING+str(i)+" files deleted."+c.ENDC+"\n"
        
# Method: Fetch
# Purpose: Download logs
# Parameters: none
# Return: none
def Fetch():
    # Make sure 'logs' directory exists
    if (not isdir("./logs")):
        mkdir("./logs")

    # Instantiate a new session
    session = GetSession()
    s3 = session.resource('s3')
    b = s3.Bucket('logs.zacs.site')

    # Iterate over each object in the bucket
    for file in b.objects.all():
        # If the file does not exist on the local machine, downlaod it
        if (not isfile("."+file.key)):
            print "%sDownloading%s %s%s%s to location %s%s%s" % (c.OKGREEN, c.ENDC, c.UNDERLINE, file.key, c.ENDC, c.UNDERLINE, "."+file.key, c.ENDC)
            b.download_file(file.key, "."+file.key)

# Method: GetCommonLogFormat
# Purpose: Return log in Command Log Format
# Parameters: 
# - data: Dictionary of fields in Amazon S3 Server Access Log Format (String)
# Return: Log in Common Log Format (String)
def GetCommonLogFormat(data):
    return data["remote_ip"]+" user-identifier - ["+data["timestamp"]+"] \""+data["request_uri"]+"\" "+data["http_status"]+" "+data["object_size"]

# Method: GetCombinedLogFormat
# Purpose: Return log in Combined Log Format
# Parameters: 
# - data: Dictionary of fields in Amazon S3 Server Access Log Format (String)
# Return: Log in Combined Log Format (String)
def GetCombinedLogFormat(data):
    return data["remote_ip"]+" user-identifier - ["+data["timestamp"]+"] \""+data["request_uri"]+"\" "+data["http_status"]+" "+data["object_size"]+" \""+data["referrer"]+"\" \""+data["user_agent"]+"\""

# Method: GetSession
# Purpose: Establish an S3 session, and return it to the user
# Parameters: none
# Return: Established S3 session (Session)
def GetSession():
    # Import functions for S3 session
    from boto3.session import Session
    import boto3

    # Private access key information
    ACCESS_KEY = 'AKIA4K7UTVOAUNQFLO7T'
    SECRET_KEY = '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'

    return Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Method: Parse
# Purpose: Parse logs
# Parameters: none
# Return: none
def Parse():
    # Open combined output log file
    output_log = open("master.log", "w").close()
    output_log = open("master.log", "a")

    # Sort the logs by timestamp, with oldest logs first
    logs = sorted(listdir("./logs"))
    
    # Iterate through the sorted log list
    for log in logs:
        # Open each log
        print c.OKGREEN+"Opening"+c.ENDC+" "+c.UNDERLINE+"./logs/"+log+c.ENDC
        with open("./logs/"+log, "r") as fd:
            # Parse each entry
            for line in fd:
                d = AssociateGroups(CaptureGroups(line))
                # output_log.write(GetCommonLogFormat(d)+'\n')
                if (d["host_header"] == "s3.us-east-2.amazonaws.com"):
                    continue
                output_log.write(GetCombinedLogFormat(d)+'\n')

    output_log.close()

# Method: PrintLog
# Purpose: Pretty print dictionary of Amazon S3 Server Access
# Log Format fields
# Parameters: 
# - data: Dictionary of fields in Amazon S3 Server Access Log Format (String)
# Return: none
def PrintLog(data):
    print "On",data["timestamp"].replace(":", " ", 1),"the machine",data["remote_ip"],"(referred by",data["referrer"]+")","said",data["request_uri"],"and the server responded with",data["key"],"of size",data["object_size"],"bytes which took",data["turnaround_time"],"milliseconds to send, and resulted in the response code",data["http_status"],"and error code",data["error_code"]

# Method: Deploy
# Purpose: Send updated site to server
# Parameters: none
# Return: none
def Deploy():
    from os import walk, devnull
    import subprocess
    from sys import stdout, exit
    from Hash import HashFiles

    FNULL = open(devnull, 'w')

    # Mirror the ./local directory structure
    for path, subdirs, files in walk("./local"):
        if (len(subdirs) == 0):
            CreateTree(path.replace("./local", "./deploy"))

    # Keep track of number of files deployed
    i = 0

    # Instantiate a new S3 session
    session = GetSession()
    s3 = session.resource('s3')
    b = s3.Bucket('zacs.site')

    # Take all HTML, XML, and JavaScript files from the ./stage
    # directory, and upload them with the appropriate headers
    for path, subdirs, files in walk("./stage"):
        if (len(files) == 0):
            print c.FAIL+"No files staged in "+path+c.ENDC
            exit(0)

        for file in files:
            # Ignore directories and hidden files
            if (file in subdirs or file[0] == "."):
                continue
            
            # Store filenames as variables
            src = "/".join([path, file])
            dst = src.replace("./stage", "./deploy")
            
            # Set content type and encoding for html, xml, and
            # js files. Ignore all others.
            content_encoding = ""
            if (file[-4:] == "html"):
                content_type = "text/html"
                content_encoding = "gzip"
            elif (file[-3:] == "xml"):
                content_type = "application/xml"
            elif (file[-2:] == "js"):
                content_type = "application/javascript"
            else:
                continue

            # Ignore files that have already been deployed
            if (isfile(dst) and HashFiles(src, dst)):
                continue

            CopyFile(src, dst, False, False)

            stdout.write(c.OKGREEN+"Deploying "+c.ENDC+dst+" ...")
            b.upload_file(Filename=src, Key=dst.replace("./deploy/", ""), ExtraArgs={'CacheControl':'max-age=2592000','ContentType':content_type, 'ContentEncoding':content_encoding})
            stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
            i += 1

    print "\n"+c.OKGREEN+str(i)+" files deployed from ./stage/"+c.ENDC

    i = 0

    for path, subdirs, files in walk("./local/assets"):
        
        for file in files:
            # Ignore directories and hidden files
            if (file in subdirs or file[0] == "."):
                continue

            # Store filenames as variables
            src = "/".join([path, file])
            dst = src.replace("./local", "./deploy")

            # Ignore files that have already been deployed
            if (isfile(dst) and HashFiles(src, dst)):
                continue

            # Set content type and encoding for html, xml, js,
            # jpg, png files. Ignore all others.
            content_type = ""
            content_encoding = ""
            if (file[-4:] == "html"):
                content_type = "text/html"
                content_encoding = "gzip"
            elif (file[-3:] == "xml"):
                content_type = "text/xml"
            elif (file[-3:] == "css"):
                content_type = "text/css"
            elif (file[-2:] == "js"):
                content_type = "application/javascript"
            elif (file[-3:] == "jpg"):
                content_type = "image/jpg"
            elif (file[-3:] == "png"):
                content_type = "image/png"
            
            # Ignore files that have already been deployed
            if (isfile(dst) and HashFiles(src, dst)):
                continue

            CopyFile(src, dst, False, False)

            stdout.write(c.OKGREEN+"Deploying "+c.ENDC+dst+" ...")
            b.upload_file(Filename=src, Key=dst.replace("./deploy/", ""), ExtraArgs={'CacheControl':'max-age=2592000','ContentType':content_type, 'ContentEncoding':content_encoding})
            stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
            
            i += 1
    print "\n"+c.OKGREEN+str(i)+" files deployed from ./local/"+c.ENDC

# Method: CompressFile
# Purpose: Create a compressed version of an input file.
# Parameters:
# - tgt: Target file, uncompressed (String)
# - dst: Destination file, to be compressed (String)
# Return: none
def CompressFile(_tgt, _dst, verbose=False, mtime=False):
    from gzip import open as gopen
    from sys import stdout
    from shutil import copyfileobj as copy
    from os import utime, stat

    with open(_tgt, 'rb') as f_in, gopen(_dst, 'wb') as f_out:
        if (verbose):
            stdout.write(c.OKGREEN+"Compressing "+c.ENDC+_tgt+" -> "+_dst+" ...")
        copy(f_in, f_out)
        if (verbose):
            stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
    if (mtime):
        utime(_dst, (stat(_tgt).st_mtime, stat(_tgt).st_mtime))

# Method: CopyFile
# Purpose: Copy a file
# Parameters:
# - tgt: Target file (String)
# - dst: Destination file (String)
# Return: none
def CopyFile(_tgt, _dst, verbose=False, mtime=False):
    from os import utime, stat, devnull
    from sys import stdout
    import subprocess

    FNULL = open(devnull, 'w')

    if (verbose):
        stdout.write(c.OKGREEN+"Copying "+c.ENDC+_tgt+" -> "+_dst+" ...")
    code = subprocess.call("cp "+_tgt+" "+_dst, stdout=FNULL, stderr=FNULL, shell=True)
    if (verbose and code != 0):
        print c.FAIL+"Error copying file."+c.ENDC
        exit(1)
    if (verbose):
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
    if (mtime):
        utime(_dst, (stat(_tgt).st_mtime, stat(_tgt).st_mtime))

    FNULL.close()

# Method: Stage
# Purpose: Update site locally
# Parameters: none
# Return: none
def Stage():
    from os import utime, stat, devnull
    from ModTimes import CompareMtimes

    # Setup the environment for staging
    ## ./stage and ./stage/blog
    CreateTree("./stage/blog", True)

    # Keep track of number of files staged
    i = 0

    # Take all HTML, XML, and JavaScript files from the directory,
    # compress them, and copy the gzipped files to ./stage
    for file in listdir("./local"):
        src = "./local/"+file
        dst = "./stage/"+file
        if (isfile(dst) and CompareMtimes(src, dst)):
            continue

        if (file[-4:] == "html"):
            CompressFile(src, dst, True, True)
            i += 1
        elif (file[-3:] == "xml" or file[-2:] == "js"):
            CopyFile(src, dst, True, True)
            i += 1

    # Take all HTML files in ./blog, compress them, and copy the
    # gzipped files to ./stage
    for file in listdir("./local/blog/"):
        src = "./local/blog/"+file
        dst = "./stage/blog/"+file
        if (file[-4:] == "html"):
            if (isfile(dst) and CompareMtimes(src, dst)):
                continue
            CompressFile(src, dst, True, True)
            i += 1

    print "\n"+c.OKGREEN+str(i)+" files staged."+c.ENDC

if (__name__ == "__main__"):
    # Import functions for CLI
    from sys import argv, exit

    # Create new instance of colors, for input styling
    c = colors()

    # Store the menu in a variable so as to provide easy access at any point in time.
    menu = """
    * To view server logs:          %sview%s
    * To fetch server logs:         %sfetch%s
    * To parse server logs:         %sparse%s
    * To stage site locally:        %sstage%s
    * To clear the staged site:     %sclear%s
    * To deploy site to server:     %sdeploy%s
    """ % (c.OKGREEN, c.ENDC, c.WARNING, c.ENDC, c.WARNING, c.ENDC, c.FAIL, c.ENDC, c.FAIL, c.ENDC, c.FAIL, c.ENDC)

    # Basic input checking
    if (len(argv) <= 1):
        print c.FAIL+"Error: enter a command:"+c.ENDC
        print menu
        exit(1)
    if (len(argv) > 2):
        print c.FAIL+"Error: too many parameters."+c.ENDC
        exit(1)

    # Handle input
    ## View logs
    if (argv[1] == "view"):
        from os import system
        system("goaccess master.log -c")
    ## Fetch logs
    elif (argv[1] == "fetch"):
        Fetch()
    ## Parse logs
    elif (argv[1] == "parse"):
        Parse()
    # Stage the site
    # Also stage ./assets
    elif (argv[1] == "stage"):
        Stage()
    # Clear the ./stage and ./deploy directories
    elif (argv[1] == "clear"):
        Clear("./stage")
        Clear("./deploy")
    # Deploy the site
    # Also deploy ./assets
    elif (argv[1] == "deploy"):
        Deploy()
    ## Invalid parameter. Notify user and exit.
    else:
        print c.FAIL+"Error: enter a valid command."+c.ENDC
        exit(1)