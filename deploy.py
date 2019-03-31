#!/usr/bin/python

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

# Method: Fetch
# Purpose: Download logs
# Parameters: none
# Return: none
def Fetch():
    # Import functions for file operations
    from os.path import isdir, isfile
    from os import mkdir
    
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
            print "Downloading '%s' to location '%s'" % (file.key, "."+file.key)
            b.download_file(file.key, "."+file.key)

# Method: GetChangedFiles
# Purpose: Return a list of files modified since last push
# Parameters: none
# Return:
# - send: File names that have changed since last commit (Array)
def GetChangedFiles():
    from os import devnull
    import subprocess
    FNULL = open(devnull, 'w')

    send = []

    code = subprocess.call("git status", stdout=FNULL, stderr=FNULL, shell=True)
    if (code != 0):
        print "Error with source control configuration: no repository found."
        exit(1)

    output = subprocess.check_output("git status", shell=True)
    if ("Changes not staged for commit" not in output):
        print "Nothing to update."
        exit(1)

    # Isolate the "modified: " section of "git status" output
    files = output.split("modified:", 1)[1].strip().split('\n')
    files = files[0:files.index('')]

    # Extract the filenames from the "modified: " section
    for i,file in enumerate(files, start=0):
        files[i] = file.replace("modified:", "").strip()

    for file in files:
        if (file[-4:] == "html" and "system/" not in file):
            send.append(file)

    FNULL.close()

    return send

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
    # Import functions for file operations
    from os import listdir

    # Open combined output log file
    output_log = open("master.log", "w").close()
    output_log = open("master.log", "a")

    # Sort the logs by timestamp, with oldest logs first
    logs = sorted(listdir("./logs"))
    
    # Iterate through the sorted log list
    for log in logs:
        # Open each log
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

# Method: Push
# Purpose: Send updated site to server
# Parameters: none
# Return: none
def Push():
    send = GetChangedFiles()
    if (send == []):
        print "No files to push."
        exit(0)

    print send

    # Instantiate a new session
    session = GetSession()
    s3 = session.resource('s3')
    b = s3.Bucket('zacs.site')

    for each in send:
        # print "Command to execute: '%s'" % ("b.upload_file(Filename="+each+", Key="+each+", ExtraArgs={Cache-Control:'max-age=2592000'})")
        print "Uploading",each,"as",each[6:]
        b.upload_file(Filename=each, Key=each[6:], ExtraArgs={'CacheControl':'max-age=2592000','ContentEncoding':'gzip','ContentType':'text/html'})
        print "Finished uploading",each

# Method: Stage
# Purpose: Update site locally
# Parameters: none
# Return: none
def Stage():
    from os.path import isdir
    from os import mkdir, listdir
    from gzip import open as gopen
    from shutil import copyfileobj as copy

    # Setup the environment for staging
    ## If the ./stage directory doesn't exist, create it
    if (not isdir("./stage")):
        mkdir("./stage")
    ## If the ./stage/blog directory doesn't exist, create it
    if (not isdir("./stage/blog")):
        mkdir("./stage/blog")

    # Take all HTML, XML, and JavaScript files from the directory,
    # compress them, and move the gzipped files to ./stage
    for file in listdir("./"):
        if (file[-4:] == "html" or file[-3:] == "xml" or file[-2:] == "js"):
            with open(file, 'rb') as f_in, gopen('./stage/'+file, 'wb') as f_out:
                copy(f_in, f_out)

    # Take all HTML files in ./blog, compress them, and move the
    # gzipped files to ./stage
    for file in listdir("./blog/"):
        if (file[-4:] == "html"):
            with open("./blog/"+file, 'rb') as f_in, gopen('./stage/blog/'+file, 'wb') as f_out:
                copy(f_in, f_out)

if (__name__ == "__main__"):
    # Import functions for CLI
    from sys import argv, exit

    # Create new instance of colors, for input styling
    c = colors()

    # Store the menu in a variable so as to provide easy access at any point in time.
    menu = """
    * To view server logs:      %sview%s
    * To fetch server logs:     %sfetch%s
    * To parse server logs:     %sparse%s
    * To deploy site:           %sdeploy%s
    """ % (c.OKGREEN, c.ENDC, c.WARNING, c.ENDC, c.WARNING, c.ENDC, c.FAIL, c.ENDC)

    # Basic input checking
    if (len(argv) <= 1):
        print c.FAIL+"Error: enter a command:"+c.ENDC
        print menu
        exit(1)
    if (len(argv) > 2):
        print c.FAIL+"Error: too many parameters."+c.ENDC
        exit(1)

    # Handle input
    ## Fetch logs
    if (argv[1] == "fetch"):
        Fetch()
    ## Parse logs
    elif (argv[1] == "parse"):
        Parse()
    ## View logs
    elif (argv[1] == "view"):
        from os import system
        system("goaccess master.log -c")
    # Stage the site
    elif (argv[1] == "stage"):
        Stage()
    # Push the site
    elif (argv[1] == "push"):
        Push()
    ## Invalid parameter. Notify user and exit.
    else:
        print c.FAIL+"Error: enter a valid command."+c.ENDC
        exit(1)

