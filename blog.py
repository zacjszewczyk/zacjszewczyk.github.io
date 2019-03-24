#!/usr/bin/env python

# Imports
# Todo: Only import functions from modules that I actually need, not entire module
from os import listdir, stat, remove, utime # File operations
from time import strptime, strftime, mktime, localtime # Managing file modification time
import datetime # Recording runtime
from re import search # Regex
from sys import exit, argv # Command line options
from Markdown import Markdown

# Global variables
# - types: Keep track of current and two previous line types. (Tuple)
# - active: Keep track of active block-level HTML element. (String)
# - file_idx: Current file number. (Int)
# - files: Dictionary with years as the keys, and sub-dictinaries as the 
#          elements. These elements have months as the keys, and a list
#          of the posts made in that month as the elements. (Dictionary)
# - months: A dictionary for converting decimal (string) representations
#           of months to their names. (Dictionary)
# - content: A string with the opening and closing HTML tags. (String)
types = ["", "", ""]
active = ""
file_idx = 0
files = {}
months = {"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June","07":"July","08":"August","09":"September","10":"October","11":"November","12":"December"}
content = ""

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

# Method: AppendContentOfXToY
# Purpose: Append the first paragraph of an original article, or
#          the entirety of a linkpost, to a target file.
# Parameters:
# - target: Target file name, including extension. (String)
# - source: Source file name, including extension. (String)
def AppendContentOfXToY(target, source):
    # Initialize file descriptors for the source and target files.
    source_fd = open("Content/"+source, "r")
    target_fd = open("Structure/"+target+".html", "a")

    # Initialize method variables.
    ptype = "linkpost"
    idx = 0
    title = ""

    # Iterate over each line in the source content file.
    for line in iter(source_fd.readline, ""):
        # In the first line, classify the article as a linkpost or an original piece.
        if (idx == 0):
            if (line[0:5] != "Type:"):
                ptype = Migrate(source, mod_time).strip()
            else:
                ptype = line.replace("Type: ", "").strip()
            title += "<article>\n    <h2 style=\"text-align:center;\">\n        <a href=\"{{URL}}\" class=\"%s\">{{URL_TITLE}}</a>" % (line.replace("Type: ", "").strip())
        # In the second line of the file, add the article title.
        elif (idx == 1):
            title = title.replace("{{URL_TITLE}}", line.replace("Title: ", "").strip())
        # In the third line of the file, add the article URL to the title/link.
        elif (idx == 2):
            title = (title.replace("{{URL}}", "/blog/"+source.lower().replace(" ", "-").replace(".txt", "")), title.replace("{{URL}}", line.replace("Link: ", "").strip()))[ptype == "linkpost"]+"\n    </h2>"
            url = (("/blog/"+source.lower().replace(" ", "-").replace(".txt", "")), title.replace("{{URL}}", line.replace("Link: ", "").strip()))[ptype == "linkpost"]
        # In the fourth line of the file, read the pubdate, and add it to the article.
        elif (idx == 3):
            line = line.replace("Pubdate: ", "").replace(" ", "/").split("/")
            title += """\n    <time datetime="%s-%s-%s" pubdate="pubdate">By <link rel="author">Zac J. Szewczyk</link> on <a href="%s">%s</a>/<a href="%s">%s</a>/%s %s</time>""" % (line[0], line[1], line[2], "/blog/"+line[0], line[0], "/blog/"+line[0]+"/"+line[1], line[1], line[2], line[3])
        # In the fifth line of the file, write the opening tags to the target, then the file's
        # content as generated up to this point.
        elif (idx == 4):
            target_fd.write(title.strip()+"\n")
        # Skip the fifth line of the file. It's blank.
        # Parse the sixth line of the file, the first paragraph, as Markdown. Write
        # it to the target file.
        elif (idx == 6):
            target_fd.write("\n    "+Markdown(line).replace("#fn", url+"#fn"))
        # For successive lines of the file, if the article is a linkpost, parse
        # them as Markdown and write them to the file.
        elif (idx > 6 and ptype == "linkpost"):
            target_fd.write("\n    "+Markdown(line).replace("#fn", url+"#fn"))

        # Increase the file index
        idx += 1
    else:
        # At the end of the file, append the read more link and the closing HTML tags.
        target_fd.write("\n    <p class='read_more_paragraph'>\n        <a style='text-decoration:none;' href='/blog/%s'>&#x24E9;</a>\n    </p>" % (source.lower().replace(" ", "-").replace(".txt", "")))
        target_fd.write("\n</article>\n")

    # Close the file descriptors.
    target_fd.close()
    source_fd.close()

# Method: AppendToFeed
# Purpose: Append the content of a source file to the RSS feed.
# Parameters:
# - source: Source file name, including extension. (String)
def AppendToFeed(source):
    # Initialzie file descriptors for the source content file and the RSS feed
    source_fd = open("Content/"+source, "r")
    feed_fd = open("Static/Main_feed.xml", "a")

    # Initialize method variables
    ptype = "linkpost"
    idx = 0

    # Create a new item in the RSS feed
    feed_fd.write("        <item>\n")

    # For each line in the content file, parse it from Markdown to HTML to XML
    # for the feed.
    for line in iter(source_fd.readline, ""):
        # Escape ampersands.
        if ("&" in line):
            line = line.replace("&", "&#38;")
        
        # In the first line, classify the article as a linkpost or an original piece.
        if (idx == 0):
            ptype = line.replace("Type: ", "").strip()
        # In the second line of the file, add the article title.
        elif (idx == 1):
            feed_fd.write("            <title>"+line.replace("Title: ", "").strip()+"</title>\n")
        # In the third line of the file, add the article URL to the title/link.
        elif (idx == 2):
            if (ptype == "linkpost"):
                if (line[0:7] != "http://"):
                    line = "http://"+line
                feed_fd.write("            <link>"+line.replace("Link: ", "").strip()+"</link>\n")
                feed_fd.write("            <guid>"+line.replace("Link: ", "").strip()+"</guid>\n")
            else:
                feed_fd.write("            <link>http://zacjszewczyk.com/blog/"+source.lower().replace(" ", "-").replace(".txt", "").lower()+"</link>\n")
                feed_fd.write("            <guid>http://zacjszewczyk.com/blog/"+source.lower().replace(" ", "-").replace(".txt", "").lower()+"</guid>\n")
        # Close the <description> portion of the item.
        # In the fourth line of the file, read the pubdate, and add it to the article.
        elif (idx == 3):
            feed_fd.write("            <description>")
        # Ignore the rest of the header, until the first line of content.
        # Write the first paragraph to the file.
        elif (idx == 6):
            feed_fd.write("\n                "+Markdown(line).replace("&", "&#38;").replace("<", "&lt;").replace(">", "&gt;"))
        # If a linkpost, write successive lines to the file.
        elif (idx > 6 and ptype == "linkpost"):
            feed_fd.write("\n                "+Markdown(line).replace("&", "&#38;").replace("<", "&lt;").replace(">", "&gt;"))
        
        # Increase the line number
        idx += 1

    # At the end of the file, write closing XML tags.
    else:
        feed_fd.write("\n            </description>\n        </item>\n")

    # Close the file descriptors.
    feed_fd.close()
    source_fd.close()

# Method: BuildFromTemplate
# Purpose: Build a target file, with a specified title and body id, and
# optional fields for inserted stylesheets and content
# Parameters:
# - target: Target file name, including extension. (String)
# - title: Value used in meta title field, and <title> element. (String)
# - bodyid: ID for body element. (String)
# - sheets: Any stylesheets to be inserted into the <head> element. (String)
# - passed_content: Body content to insert into the <body> element. (String)
def BuildFromTemplate(target, title, bodyid, sheets="", passed_content=""):
    # Make global variable accessible within the method
    global content

    # Clear the target file, then write the opening HTML code and any passed content.
    fd = open("Structure/"+target, "w").close()
    fd = open("Structure/"+target, "a")
    fd.write(content[0].replace("{{ title }}", title).replace("{{ BODYID }}", bodyid).replace("<!-- SHEETS -->", sheets))
    fd.write(passed_content)
    fd.close()

# Method: CloseTemplateBuild
# Purpose: Open the target file and write the closing HTML to it, with an
#          optional field for inserted scripts.
# Parameters:
# - target: Target file name, including extension. (String)
# - scripts: Any Javascript to be inserted below the <body> element. (String)
def CloseTemplateBuild(target, scripts=""):
    # Make global variable accessible within the method
    global content

    # Write the trailing HTML tags from the template to the target file.
    fd = open("Structure/"+target, "a")
    fd.write(content[1].replace("<!-- SCRIPTS BLOCK -->", scripts))
    fd.close()

# Method: GenBlog
# Purpose: Generate the blog.
# Parameters: none
def GenBlog():
    # Make global variables accessible in the method, and initialize method variables.
    global files
    global file_idx
    global content

    # Sort the files dictionary by keys, year, then iterate over it
    for year in sorted(files, reverse=True):
        # For each year in which a post was made, generate a 'year' file, that
        # contains links to each month in which a post was published.

        # Clear the 'year' file
        year_fd = open("Structure/"+year+".html", "w").close()
        year_fd = open("Structure/"+year+".html", "a")
        # Write the opening HTML tags
        year_fd.write(content[0].replace("{{ title }}", "Post Archives - ").replace("{{ BODYID }}", "archives"))
        # Insert a 'big table' into the document, to better display the months listed.
        year_fd.write("""<table style="width:100%;padding:20pt 0;" id="big_table">""")
        year_fd.write("    <tr>\n        <td>%s</td>\n    </tr>\n" % (year))
        # Sort the sub-dictionaries by keys, months, then iterate over it. For each
        # month in which a post was made, generate a 'month' file that contains all
        # posts made during that month.
        for month in sorted(files[year], reverse=True):
            # Add a link to the month, to the year file it belongs to.
            year_fd.write("    <tr>\n        <td><a href=\"%s\">%s</a></td>\n    </tr>\n" % ("/blog/"+year+"/"+month, months[month]))
            # Clear the 'month' file
            month_fd = open("Structure/"+year+"-"+month+".html", "w").close()
            month_fd = open("Structure/"+year+"-"+month+".html", "a")
            # Write the opening HTML tags
            month_fd.write(content[0].replace("{{ title }}", "Post Archives - ").replace("{{ BODYID }}", "archives").replace("<!--BLOCK HEADER-->", "<article>\n<p>\n"+months[month]+", <a href=\"/blog/"+year+"\">"+year+"</a>\n</p>\n</article>"))
            
            # Sort the sub-dictionaries by keys, days, then iterate over it.
            for day in sorted(files[year][month], reverse=True):
                # Sort the sub-dictionaries by keys, timestamps, then iterate over it
                for timestamp in sorted(files[year][month][day], reverse=True):
                    # For each article made in the month, add an entry on the appropriate
                    # 'month' structure file.
                    month_fd.write("<article>\n    %s<a href=\"%s\">%s</a>\n</article>\n" % (year+"/"+month+"/"+day+" "+timestamp+": ", "/blog/"+files[year][month][day][timestamp].lower().replace(" ", "-").replace(".txt", ""), GetTitle(files[year][month][day][timestamp])))
                    # Generate each content file. "year", "month", "day", "timestamp"
                    # identify the file in the dictionary, and the passed time values
                    # designate the desired update time to set the content file.
                    GenPage(files[year][month][day][timestamp], "%s/%s/%s %s" % (year, month, day, timestamp))
                    
                    # Add the first twenty-five articles to the main blog page.
                    if (file_idx < 25):
                        AppendContentOfXToY("blog", files[year][month][day][timestamp])
                    # Write the years in which a post was made to the header element, in a
                    # big table to facilitate easy reading. 
                    elif (file_idx == 25):
                        # This block just puts three year entries in the first row, ends
                        # the row, and then puts three more year entries in the second row.
                        # This code is stored in 'buff', and then added to the archives
                        # page.
                        buff = """\n<article>\n<table style="width:100%;padding:2% 0;" id="big_table">\n    <tr>\n"""
                        for each in sorted(files, reverse=True)[:3]:
                            buff += """\n        <td>\n            <a href=\"/blog/%s\">%s</a>\n        </td>""" % (each.lower(), each)
                        buff += """\n    </tr>\n    <tr>\n"""
                        for each in sorted(files, reverse=True)[3:]:
                            buff += """\n        <td>\n            <a href=\"/blog/%s\">%s</a>\n        </td>""" % (each.lower(), each)
                        buff += """\n    </tr>\n</table>\n</article>\n"""
                        archives_fd = open("Structure/archives.html", "a")
                        archives_fd.write(buff)
                        archives_fd.write("<article style='text-align:center;padding:20pt;font-size:200%%;'><a href='/blog/%s'>%s</a></article>" % (year, year))
                        archives_fd.close()
                        temp = year

                        # Add the twenty-sixth article to the archives page.
                        AppendContentOfXToY("archives", files[year][month][day][timestamp])
                    
                    # Add all other articles to the archives page.
                    else:
                        if (temp != year):
                            archives_fd = open("Structure/archives.html", "a")
                            archives_fd.write("<article style='text-align:center;padding:20pt;font-size:200%%;'><a href='/blog/%s'>%s</a></article>" % (year, year))
                            archives_fd.close()
                            temp = year
                        AppendContentOfXToY("archives", files[year][month][day][timestamp])
                    
                    # Add all articles to the RSS feed.
                    AppendToFeed(files[year][month][day][timestamp])
                    
                    # Increase the file index.
                    file_idx += 1
            
            # Write closing HTML tags to the month file.
            month_fd.write(content[1])
            month_fd.close()
        
        # Write closing HTML tags to the year file.
        year_fd.write("</table>\n"+content[1])
        year_fd.close()

    # Write closing HTML Tags to archives.html and blog.html, using Terminate()
    Terminate()

# Method: GenPage
# Purpose: Given a source content file, generate a corresponding HTML structure file.
# Parameters:
# - source: Filename of the source content file. (String)
# - timestamp: Timestamp for reverting update time, format %Y/%m/%d %H:%M:%S. (String)
def GenPage(source, timestamp):
    global content

    # Ensure source file contains header. If not, use the Migrate() method to generate it.
    source_fd = open("Content/"+source, "r")
    line = source_fd.readline()
    if (line[0:5] != "Type:"):
        Migrate(source, timestamp)
    source_fd.close()
    
    # Open the source file in read mode.
    source_fd = open("Content/"+source, "r")

    # Use the source file's name to calculate, clear, and re-open the structure file.
    target_fd = open("Structure/"+source.lower().replace(" ", "-").replace(".txt", ".html"), "w").close()
    target_fd = open("Structure/"+source.lower().replace(" ", "-").replace(".txt", ".html"), "a")

    # Insert Javascript code for device detection.
    local_content = content[0].replace("<!-- SCRIPTS -->", """\n            <script type="text/javascript">\n                function insertAfter(e,a){a.parentNode.insertBefore(e,a.nextSibling)}for(var fn=document.getElementsByClassName("footnote"),i=0;i<fn.length;i++){var a=[].slice.call(fn[i].children);if("[object HTMLParagraphElement]"==a[a.length-1]){var temp=a[a.length-2];a[a.length-2]=a[a.length-1],a[a.length-1]=temp;for(var j=0;j<a.length;j++)fn[i].removeChild(a[j]);for(var j=0;j<a.length;j++)fn[i].appendChild(a[j])}}\n                //https://www.dirtymarkup.com/, http://jscompress.com/\n                if (document.title.search("Ipad")) {document.title = document.title.replace("Ipad", "iPad")}\n            </script>""").replace("{{ BODYID }}", "post")
    
    # Initialize idx to track line numbers, and title to hold the title block of each article.
    idx = 0
    title = ""

    # Iterate over each line in the source content file.
    for line in iter(source_fd.readline, ""):
        # In the first line, classify the article as a linkpost or an original piece.
        if (idx == 0):
            title += "<article>\n    <h2 style=\"text-align:center;\">\n        <a href=\"{{URL}}\" class=\"%s\">{{URL_TITLE}}</a>" % (line.replace("Type: ", "").strip())
        # In the second line of the file, add the article title.
        elif (idx == 1):
            title = title.replace("{{URL_TITLE}}", line.replace("Title: ", "").strip())
            local_content = local_content.replace("{{ title }}", line.replace("Title: ", "").strip()+" - ")
        # In the third line of the file, add the article URL to the title/link.
        elif (idx == 2):
            line = line.replace("Link: ", "").strip()
            if (line[0:4] != "http" and ("txt" == line[-3:])):
                line = line.replace(".htm", "").replace(" ", "-").lower()
            title = title.replace("{{URL}}", line)+"\n    </h2>"
        # In the fourth line of the file, read the pubdate, and add it to the article.
        elif (idx == 3):
            # print line
            line = line.replace("Pubdate: ", "").replace(" ", "/").split("/")
            title += """\n    <time datetime="%s-%s-%s" pubdate="pubdate">By <link rel="author">Zac J. Szewczyk</link> on <a href="%s">%s</a>/<a href="%s">%s</a>/%s %s</time>""" % (line[0], line[1], line[2], "/blog/"+line[0], line[0], "/blog/"+line[0]+"/"+line[1], line[1], line[2], line[3])
        # In the fifth line of the file, write the opening tags to the target, then the file's
        # content as generated up to this point.
        elif (idx == 4):
            target_fd.write(local_content)
            target_fd.write(title.strip()+"\n")
        # For successive lines of the file, parse them as Markdown and write them to the file.
        elif (idx > 4):
            target_fd.write("\n    "+Markdown(line))

        # Increase the line number
        idx += 1
    else:
        # At the end of the file, write closing HTML tags.
        target_fd.write("\n</div>\n</article>")
        target_fd.write(content[1])
        
    # Close file descriptors.
    target_fd.close()
    source_fd.close()

# Method: GenStatic
# Purpose: Create home, projects, and error static structure files.
# Parameters: none
def GenStatic():
    # Reference the home.html source file to generate the front-end structure file.
    fd = open("Structure/system/home.html", "r")
    home = fd.read().split("<!-- DIVIDER -->")
    fd.close()
    BuildFromTemplate("home.html", "", "home", sheets=home[0], passed_content=home[1])

    # Reference the projects.html source file to generate the front-end structure file.
    fd = open("Structure/system/projects.html", "r")
    projects = fd.read().split("<!-- DIVIDER -->")
    fd.close()
    BuildFromTemplate("projects.html", "Projects - ", "projects", "", passed_content=projects[1])

    # Build the error.html file.
    BuildFromTemplate("error.html", "Error - ", "error", "", "")
    CloseTemplateBuild("error.html", """<script type="text/javascript">document.getElementById("content_section").innerHTML = "<article><h2 style=\"text-align:center;\">Error: 404 Not Found</h2><p>The requested resource at <span style="text-decoration:underline;">"+window.location.href+"</span> could not be found.</p></article>"</script>""")

# Method: GetUserInput
# Purpose: Accept user input and perform basic bounds checking
# Parameters:
# - prompt: Text to prompt the user for input (String)
def GetUserInput(prompt):
    c = colors()

    # Prompt the user for valid input
    while True:
        string = raw_input(prompt)
        
        # Do not allow empty strings
        if (len(string) == 0):
            print c.WARNING+"Input cannot be empty."+c.ENDC
            continue
        # Do not allow more than 32 characters
        elif (len(string) > 32):
            print c.WARNING+"Input bound exceeded."+c.ENDC
            continue
        # If we get here, we have valid input
        break
    return string

# Method: GetFiles
# Purpose: Return the global variable files, to make it accessible in a method
# Parameters: none
def GetFiles():
    global files
    return files

# Method: GetTitle
# Purpose: Return the article title of a source file.
# Parameters:
# - source: Source file name, including extension. (String)
def GetTitle(source):
    # Open a source file and return the article's title.
    fd = open("Content/"+source, "r")
    fd.readline()
    title = fd.readline().replace("Title: ", "")
    fd.close()
    return title

# Method: Init
# Purpose: Instantiate the global variable 'content', to reduce duplicate I/O
#          operations. Then clear the blog and archive structure files, and
#          the RSS feed, and write the opening tags. Generate file dictionary.
# Parameters: none
def Init():
    # Make global variables accessible in the method, and initialize method variables.
    global file_idx, files, content
    file_idx = 0
    files = {}

    # Open the template file, split it, and store each half in a list.
    fd = open("Structure/system/template.htm", "r")
    content = fd.read()
    content = content.split("<!--Divider-->")
    content.append(content[0])
    fd.close()

    # Clear and initialize the archives.html and blog.html files.
    BuildFromTemplate("archives.html", "Post Archives - ", "postarchives")
    BuildFromTemplate("blog.html", "Blog - ", "blog")
    
    # Clear and initialize the RSS feed
    fd = open("Static/Main_feed.xml", "w")
    fd.write("""<?xml version='1.0' encoding='ISO-8859-1' ?>\n<rss version="2.0" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n    <title>Zac J. Szewczyk</title>\n    <link>http://zacjszewczyk.com/</link>\n    <description></description>\n    <language>en-us</language>\n    <atom:link href="http://zacjszewczyk.com/rss" rel="self" type="application/rss+xml" />\n    <lastBuildDate>%s EST</lastBuildDate>\n    <ttl>5</ttl>\n    <generator>First Crack</generator>\n""" % (datetime.datetime.now().strftime("%a, %d %b %Y %I:%M:%S")))
    fd.close()

    # FUTURE: Do this for the Structure directory, minus key system files, to determine
    # what--if anything--needs updated, rather than rebuilding the site every time.
    
    # Generate a dictionary with years as the keys, and sub-dictinaries as the elements.
    # These elements have months as the keys, and a list of the posts made in that month
    # as the elements.
    for each in listdir("Content"):
        if (".txt" in each):
            mtime = strftime("%Y/%m/%d/%H:%M:%S", localtime(stat("Content/"+each).st_mtime)).split("/")
            if (mtime[0] not in files):
                files[mtime[0]] = {}
            if (mtime[1] not in files[mtime[0]]):
                files[mtime[0]][mtime[1]] = {}
            if (mtime[2] not in files[mtime[0]][mtime[1]]):
                files[mtime[0]][mtime[1]][mtime[2]] = {}
            if (mtime[3] not in files[mtime[0]][mtime[1]][mtime[2]]):
                files[mtime[0]][mtime[1]][mtime[2]][mtime[3]] = {}
            files[mtime[0]][mtime[1]][mtime[2]][mtime[3]] = each

# Method: Interface
# Purpose: Provide a command line interface for the script, for more granular control
# of its operation.
# Parameters: params: command line parameters (String)
def Interface(params):
    # Instantiate the "colors" class, for output styling
    c = colors()

    # Store the menu in a variable so as to provide easy access at any point in time.
    menu = """
    * To search all articles:                        %s-S%s
    * To clear all structure files:                  %s-R%s
    * To display this menu:                          %s-h%s
    * To exit this mode and build the site:          %sexit%s
    * To exit this mode and quit the program:        %s!exit%s
    """ % (c.OKGREEN, c.ENDC, c.OKGREEN, c.ENDC, c.WARNING, c.ENDC, c.FAIL, c.ENDC, c.FAIL, c.ENDC)

    # Using the "-a" parameter enters Authoring mode, so print the welcome message
    if "-a" in params:
        print ("""\
Welcome to First Crack's "Authoring" mode.\n
Entering "-h" into the prompt at any point in time will display the menu below.
%s""" % (menu))

    # Continue prompting the user for input until they enter a valid argument
    while (True):
        if "-a" in params:
            query = raw_input("#: ")
        else:
            query = str(params)
        params = ""

        # Print the menu of valid commands to the terminal.
        if (search("-h", query) or search("help", query)):
            print (menu)

        # Search all articles
        if (search("-S", query) != None):
            # Get a string to search all files for
            search_string = GetUserInput("Enter string to search for: ")

            # Iterate over the entire ./Content dirctory
            for file in listdir("Content"):
                # Only inspect text files
                if (not ".txt" in file):
                    continue

                # Search each line of the file, case insensitively
                res = SearchFile(file, search_string)
                if (res):
                    print "\nFile: "+c.UNDERLINE+file+c.ENDC
                    for match in res:
                        print "    %sLine %d:%s %s" % (c.BOLD, match[0], c.ENDC, match[1])

        # Remove all existing structure files
        if (search("-R", query) != None):
            for files in listdir("Structure"):
                if (files != "system"):
                    remove("Structure/"+files)
            return False

        # Exit the command-line interface and prevent the site from rebuilding.
        if (search("!exit", query) != None):
            exit(0)
        
        # Exit the command-line interface and proceed with site build.
        if (search("exit", query) != None) or (search("logout", query) != None):
            return False
        # Accept user input again
        else:
            params = "-a"

# Method: Migrate
# Purpose: For files without the header information in their first five lines, generate
#          that information, insert it into the file, and revert the update time.
# Parameters
# - target: Target file name, including extension. (String)
# - mod_time: Timestamp for reverting update time, format %Y/%m/%d %H:%M:%S. (String)
def Migrate(target, mod_time):
    # Open the target file and read the first line.
    fd = open("Content/"+target, "r")
    article_content = fd.readline()

    # Detect a linkpost or an original article, and parse the information appropriately.
    if (article_content[0:2] == "# ["):
        article_type = "linkpost"
        article_content = article_content[2:].replace(") #", "")
        article_content = article_content.split("]")
        article_title = article_content[0][1:]
        article_url = article_content[1][1:-1]
    else:
        article_type = "original"
        article_title = article_content.replace("# ", "").replace(" #", "")
        article_url = target.replace(".txt", "").replace(" ", "-").lower()
        article_content = fd.readline()

    # Read the rest of the article's content from the file.
    article_content = fd.read()
    fd.close()

    # Clear the target file, then write it's contents into it after the header information.
    fd = open("Content/"+target, "w")
    fd.write("""Type: %s\nTitle: %s\nLink: %s\nPubdate: %s\nAuthor: %s\n\n%s""" % (article_type, article_title.strip(), article_url.strip(), mod_time, "Zac Szewczyk", article_content.strip()))
    fd.close()

    # Revert the update time for the target file, to its previous value.
    utime("Content/"+target, ((mktime(strptime(mod_time, "%Y/%m/%d %H:%M:%S"))), (mktime(strptime(mod_time, "%Y/%m/%d %H:%M:%S")))))

    # Return the read article type, for debugging.
    return article_type

# Method: SearchFile
# Purpose: Search for a string within a file.
# Parameters: 
# - tgt: Target file name (String)
# - q: String to search for (String)
def SearchFile(tgt, q):
    ret = []
    with open("Content/"+tgt) as fd:
        idx = 0
        for line in fd:
            if (q.lower() in line.lower()):
                ret.append([idx, line.strip()])
            idx += 1
    if (len(ret) == 0):
        return False
    return ret

# Method: Terminate
# Purpose: Write closing tags to blog and archives structure files.
# Parameters: none
def Terminate():
    # Write closing tags to archives.html and blog.html.
    CloseTemplateBuild("archives.html")
    CloseTemplateBuild("blog.html")
    CloseTemplateBuild("projects.html")
    CloseTemplateBuild("home.html")
    
    # Write closing tags to the RSS feed.
    fd = open("Static/Main_feed.xml", "a")
    fd.write("""\n</channel>\n</rss>""")
    fd.close()

# If run as an individual file, generate the site and report runtime.
# If imported, only make methods available to imported program.
if __name__ == '__main__':
    argv = argv
    argc = len(argv)
    if (argc > 1):
        Interface(argv[1:])

    t1 = datetime.datetime.now()
    Init()
    GenStatic()
    GenBlog()
    # import cProfile
    # cProfile.run("Init()")
    # cProfile.run("GenStatic()")
    # cProfile.run("GenBlog()")

    t2 = datetime.datetime.now()

    c = colors()
    print ("Execution time: "+c.OKGREEN+str(t2-t1)+"s"+c.ENDC)