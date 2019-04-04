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
# - d__: Dictionary of groups with the right label as their key (Dictionary)
def AssociateGroups(groups):
    d__ = {}
    labels = ["owner","bucket","timestamp","remote_ip","requester","request_id","operation","key","request_uri","http_status","error_code","bytes_sent","object_size","transmission_time","turnaround_time","referrer","user_agent","version_id","host_id","signature_version","cipher_suite","authentication_type","host_header","tls_version"]
    for i, field in enumerate(groups, start=0):
        if (i < len(labels)):
            d__[labels[i]] = field
        else:
            d__[i] = field
    return d__

# Method: CaptureGroups
# Purpose: Return array of groups from Amazon S3 Server Access Log Format
# Parameters: 
# - entry: Log in Amazon S3 Server Access Log Format
# Return: 
# - a: Array of capture groups (Array)
def CaptureGroups(entry):
    delimeters = ['"', '[', ']', ' ']
    group = ""
    end = ' '
    a = []
    for character in entry:
        if (group == "" and end == ' ' and character in delimeters):
            if (character == '['):
                end = ']'
            else:
                end = character
        elif (character == end):
            a.append(group)
            group = ""
            end = ' '
        else:
            group += character
    else:
        a.append(group.strip())
    return a

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
    for file in listdir("./stage"):
        if (file[-4:] == "html"):
            content_type = "text/html"
            content_encoding = "gzip"
        elif (file[-3:] == "xml"):
            content_type = "text/xml"
            content_encoding = ""
        elif (file[-2:] == "js"):
            content_type = "text/javascript"
            content_encoding = ""
        else:
            continue

        # Ignore files that have already been deployed
        if (isfile("./deploy/"+file) and HashFiles("./stage/"+file, "./deploy/"+file)):
            continue

        stdout.write(c.OKGREEN+"Coping file at: "+c.ENDC+"./stage/"+file+" ...")
        code = subprocess.call("cp ./stage/"+file+" ./deploy/"+file, stdout=FNULL, stderr=FNULL, shell=True)
        if (code != 0):
            print c.FAIL+"Error moving file."+c.ENDC
            exit(1)
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
        stdout.write(c.OKGREEN+"Uploading file at: "+c.ENDC+"./deploy/"+file+" ...")
        # b.upload_file(Filename="./deploy/"+file, Key=file, ExtraArgs={'CacheControl':'max-age=2592000','ContentEncoding':content_encoding,'ContentType':content_type})
        i += 1
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")

    for file in listdir("./stage/blog/"):
        # Ignore everything but HTML files
        if (file[-4:] != "html"):
            continue

        # Ignore files that have already been deployed
        if (isfile("./deploy/blog/"+file) and HashFiles("./stage/blog/"+file, "./deploy/blog/"+file)):
            continue

        stdout.write(c.OKGREEN+"Copying file at: "+c.ENDC+"./stage/blog/"+file+" ...")
        code = subprocess.call("cp ./stage/blog/"+file+" ./deploy/blog/"+file, stdout=FNULL, stderr=FNULL, shell=True)
        if (code != 0):
            print c.FAIL+"Error copying file."+c.ENDC
            exit(1)
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
        stdout.write(c.OKGREEN+"Uploading file at: "+c.ENDC+"./deploy/blog/"+file+" ...")
        # b.upload_file(Filename="./deploy/blog/"+file, Key="blog/"+file, ExtraArgs={'CacheControl':'max-age=2592000','ContentEncoding':'gzip','ContentType':'text/html'})
        i += 1
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")

    for file in listdir("./local/assets/"):
        # Ignore directories
        if (isdir("./deploy/assets/"+file)):
            continue
        # Ignore files that have already been deployed
        if (isfile("./deploy/assets/"+file)):
            continue

        if (file[-4:] == "html"):
            content_type = "text/html"
        elif (file[-3:] == "xml"):
            content_type = "text/xml"
        elif (file[-2:] == "js"):
            content_type = "text/javascript"
        else:
            content_type = ""

        stdout.write(c.OKGREEN+"Copying file at: "+c.ENDC+"./local/assets/"+file+" ...")
        code = subprocess.call("cp ./local/assets/"+file+" ./deploy/assets/"+file, stdout=FNULL, stderr=FNULL, shell=True)
        if (code != 0):
            print c.FAIL+"Error copying file."+c.ENDC
            exit(1)
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
        stdout.write(c.OKGREEN+"Uploading file at: "+c.ENDC+"./deploy/assets/"+file+" ...")
        # b.upload_file(Filename="./deploy/assets/"+file, Key="assets/"+file, ExtraArgs={'CacheControl':'max-age=2592000','ContentType':content_type})
        i += 1
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")

    for file in listdir("./local/assets/Images/"):
        # Ignore images sub-directories
        if (isdir("./local/assets/Images/"+file)):
            continue
        # Ignore files that have already been deployed
        if (isfile("./deploy/assets/Images/"+file)):
            continue

        stdout.write(c.OKGREEN+"Copying file at: "+c.ENDC+"./local/assets/"+file+" ...")
        code = subprocess.call("cp ./local/assets/Images/"+file+" ./deploy/assets/Images/"+file, stdout=FNULL, stderr=FNULL, shell=True)
        if (code != 0):
            print c.FAIL+"Error copying file."+c.ENDC
            exit(1)
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")
        stdout.write(c.OKGREEN+"Uploading file at: "+c.ENDC+"./deploy/assets/Images/"+file+" ...")
        # b.upload_file(Filename="./deploy/assets/Images/"+file, Key="assets/Images/"+file, ExtraArgs={'CacheControl':'max-age=2592000'})
        i += 1
        stdout.write(" "+c.OKGREEN+"done."+c.ENDC+"\n")

    print "\n"+c.OKGREEN+str(i)+" files deployed."+c.ENDC
    
    FNULL.close()

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