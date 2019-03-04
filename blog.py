#!/usr/bin/env python

# Imports
import os # File operations
import time # Recording runtime
import datetime # Managing file modification time
import re # Regex
import sys # Command line options

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
    for each in os.listdir("Content"):
        if (".txt" in each):
            mtime = time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime(os.stat("Content/"+each).st_mtime)).split("/")
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
    # Store the menu in a variable so as to provide easy access at any point in time.
    menu = """
    * To clear all structure files:                  -R
    * To display this menu:                          -h
    * To exit this mode and build the site:          exit
    * To exit this mode and quit the program:        !exit
    """

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
        if (re.search("-h", query) != None):
            print (menu)

        # Remove all existing structure files
        if (re.search("-R", query) != None):
            for files in os.listdir("Structure"):
                if (files != "system"):
                    os.remove("Structure/"+files)
            return False

        # Exit the command-line interface and prevent the site from rebuilding.
        if (re.search("!exit", query) != None):
            sys.exit(0)

        # Exit the command-line interface and proceed with site build.
        elif (re.search("exit", query) != None) or (re.search("logout", query) != None):
            return False
        

# Method: Markdown
# Purpose: Take a raw string from a file, formatted in Markdown, and parse it into HTML.
# Parameters:
# - Line: Line to be parsed. (String)
def Markdown(line):
    # Make global variables accessible in the method, and initialize method variables.
    # Must be global to persist between method calls.
    global types, active
    start = 1

    # Use {} to enclose an article series reference. Enclosed text identifies the article series, in the form of a file that the parser
    # opens, reads, and inserts into the actual article.
    # If line starts with {}, open target file, and return the contents with a return statement. Skip the rest w/ a return statement.

    # Part of a series
    if (line[0] == "{"):
        fd = open("Content/System/"+line[1:-1].strip(), "r")
        line = "<ul style=\"border:1px dashed gray\" id=\"series_index\">\n"
        for each in fd.read().split("\n"):
            line += "    <li>"+Markdown(each)+"</li>\n"
        line += "</ul>"
        types.append("RAW HTML")
        fd.close()
    # Header elements, <h1>-<h6>
    elif (line[0] == "#"):
        line = ("<h%d>"+line.replace("#", "").strip()+"</h%d>") % (line.split(" ")[0].count("#"), line.split(" ")[0].count("#"))+"\n"
        types.append("<h>,,</h>")
    # Images
    elif (line[0:1] == "!["):
        types.append("<img>,,</img>")
    # Footnote
    elif (re.match("(\[>[0-9]+\])", line) != None):
        types.append("<div class=\"footnote\">,,</div>")
    # Blockquotes
    elif (re.match(">|\s{4}", line) != None):
        if ((types[-1] == "<blockquote>,,</blockquote>") or (types[-1] == "<bqt>,,</bqt>")):
            types.append("<bqt>,,</bqt>")
        else:
            types.append("<blockquote>,,</blockquote>")
    # Unordered lists
    elif (re.match("\*\s", line) != None):
        line = line.replace("* ", "")
        if ((types[-1] == "<ul>,,</ul>") or (types[-2] == "<ul>,,</ul>") or (types[-3] == "<ul>,,</ul>") or (types[-1] == "<li>,,</li>") or (types[-2] == "<li>,,</li>") or (types[-3] == "<li>,,</li>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ul>,,</ul>")
    # Ordered lists
    elif (re.match("[0-9]+", line) != None):
        start = line.split(".")[0]
        line = re.sub("[0-9]+\.\s", "", line)
        if ((types[-1] == "<ol>,,</ol>") or (types[-2] == "<ol>,,</ol>") or (types[-3] == "<ol>,,</ol>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ol>,,</ol>")
    # Paragraphs
    elif (re.match("[a-zA-Z_\[\*\"]", line) != None):
        types.append("<p>,,</p>")
    # Raw HTML code.
    elif (line[0] == "<" or line[0] == "#"):
        types.append("RAW HTML")
    # A blank line. Two blank lines in a row is a linebreak.
    else:
        if (line.strip() == "" and types[-1] == "<blank>,,</blank>"):
            types.append("<br />")
        else:
            types.append("<blank>,,</blank>")

    # Managerial code to keep the 'types' tuple to 3 elements.
    if (len(types) == 4):
        types.pop(0)

    # Admin variables, for clarity's sake.
    current = types[-1]
    second = types[-2]
    third = types[-3]

    if (current != "RAW HTML"):
        # If I've already escaped a ascii code, pass; otherwise escape it.
        if (re.search("&[a-z]{4}\;", line) != None):
            pass
        elif ("&" in line):
            line = line.replace("&", "&#38;")

        # Horizontal rules
        if (line[0:3] == "---"):
            line = line.replace("---", "<hr style='margin:50px auto;width:50%;border:0;border-bottom:1px dashed #ccc;background:#999;' />")
        # Emdashes
        if ("--" in line):
            line = line.replace("--", "&#160;&#8212;&#160;")
        # Parse double-quote quotations
        for each in re.findall("([\s\<\>\\\*\/\[\-\(]+\"[\[\w\%\#\\*<\>]+)", line):
            ftxt = each.replace("\"", "&#8220;", 1)
            line = line.replace(each, ftxt)
        for each in re.findall("([\)\w+\.]+\"[\s\)\]\<\>\.\*\-\,])", line):
            ftxt = each.replace("\"", "&#8221;", 1)
            line = line.replace(each, ftxt)
        # Parse single-quote quotations
        for each in re.findall("(\w+'[\w+|\s+])", line):
            ftxt = each.replace("\'", "&#8217;")
            line = line.replace(each, ftxt)
        for each in re.findall("([\s\(]'\w+)", line):
            ftxt = each.replace("\'", "&#8216;", 1)
            line = line.replace(each, ftxt)
        # Interpret inline code
        for each in re.findall("\%[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\%", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("%", "<span class='command'>", 1)
            ftxt = ftxt.replace("%", "</span> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)            
        # Interpret <strong> tags
        for each in re.findall("\*\*{1}[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\*\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("**", "<strong>", 1)
            ftxt = ftxt.replace("**", "</strong> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)            
        # Interpret <em> tags
        for each in re.findall("\*{1}[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("*", "<em>", 1)
            ftxt = ftxt.replace("*", "</em> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)
        # Parse images, both local and remote
        for each in re.findall("(\!\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]+\]\(['\(\)\#\;?\@\%\w\&:\,\./\~\s\"\!\#\=\+-]+\))", line):
            desc = each.split("]")[0][2:]
            url = each.split("]")[1].split(" ")[0][1:]
            if (url.startswith("http://zacjszewczyk.com/")):
                # print url.split("/")[-1]
                url = """/Static/Images/%s""" % (url.split("/")[-1])
            alt = each.split("]")[1].split(" &#8220;")[1].rstrip("&#8221;)")
            line = line.replace(each, "<div class=\"image\"><img src=\""+url+"\" alt=\""+alt+"\" title=\""+desc+"\"></div>")
        # This needs some attention to work with the new URL scheme
        # Parse links, both local and remote
        for each in re.findall("""(\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]*\])(\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12\s*)?\))""", line):
            desc = each[0][1:-1]
            url = each[1][1:-1].replace("&", "&amp;").strip()
            
            if ("http://" != url[0:7] and "https://" != url[0:8]):
                if (".txt" != url[-4:]):
                    if (".htm" == url[-4:]):
                        url = "/blog/"+url.replace(" ", "-").replace(".htm", "").lower()
                else:
                    url = "/blog/"+url.replace(" ", "-").replace(".txt", "").lower()

            if (".txt" == url[-4:]):
                url = url.replace(".txt", "").replace(" ", "-").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+url.replace(" ", "-")+"\">"+desc+"</a>")
            elif (url == ""):
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+desc.replace("<em>", "").replace("</em>", "").replace(" ", "-")+"\">"+desc+"</a>")
            else:
                line = line.replace(each[0]+each[1], "<a href=\""+url+"\">"+desc+"</a>")
        # Parse footnotes
        for each in re.findall("(\[\^[0-9]+\])", line):
            mark = each[2:-1]
            url = """<sup id="fnref"""+mark+""""><a href="#fn"""+mark+"""" rel="footnote">"""+mark+"""</a></sup>"""
            line = line.replace(each, url)
        # Parse single-line comments
        if (line[0:2] == "//"):
            line = line.replace("//","<!--")+" -->"
    else:
        # Account for iframes
        if ("<iframe" == line[0:7]):
            line = "<div style='text-align:center;'>"+line+"</div>"
        elif ("<ul" == line[0:2]):
            pass
        elif (line[0:4] == "<pre"):
            pass
        # Anything else should be a blockquote
        else:
            line = "<blockquote>"+line+"</blockquote>"
    # If a paragraph
    if (current == "<p>,,</p>"):
        line = active+"\n"+current.replace(",,", line.strip())
        active = ""
    # If an unordered list
    elif (current == "<ul>,,</ul>"):
        active = "</ul>"
        line = current.split(",,")[0].replace(">", " start='"+str(start)+"'>")+"\n<li>"+line.strip()+"</li>"
    # If an ordered list
    elif (current == "<ol>,,</ol>"):
        active = "</ol>"
        line = current.split(",,")[0]+"\n<li>"+line.strip()+"</li>"
    # If a list item
    elif (current == "<li>,,</li>"):
        line = current.replace(",,", line.strip())
    # If an element following a list item
    elif ((current != "<li>,,</li>") and ((second == "<li>,,</li>") or (second == "<ul>,,</ul>") or (second == "<ol>,,</ol>"))):
        line = line.strip()+active+"\n"
        active = ""
    # If a blockquote
    elif (current == "<blockquote>,,</blockquote>"):
        active = "</blockquote>"
        line = current.split(",,")[0]+"\n<p>"+line[2:].strip()+"</p>"
    # If the continuation of a blockquote
    elif (current == "<bqt>,,</bqt>"):
        line = "<p>"+line.strip().replace("> ", "", 1)+"</p>"
    # If an element following a blockquote
    elif ((current != "<bqt>,,</bqt>") and ((second == "<bqt>,,</bqt>") or (second == "<blockquote>,,</blockquote>"))):
        line = line.strip().replace("> ", "")+"</blockquote>\n"
        active = ""
    # If a footnote
    elif ((current == "<div class=\"footnote\">,,</div>")):
        active = "</div>"
        mark = int(line.split("]")[0][2:])
        line = line.split("]")[1]
        # If the first footnote
        if (mark == 1): 
            line = current.split(",,")[0].replace("div ", "div id=\"fn"+str(mark)+"\" ")+"\n<p>"+line.strip()+"""</p><a class="fn" title="return to article" href="#fnref"""+str(mark)+"""">&#x21a9;</a>"""
        # If a later footnote
        else: 
            line = "</div>"+current.split(",,")[0]+"<p>"+line.strip()+"</p>"
            line = line.replace("div ", "div id=\"fn"+str(mark)+"\" ")+"""<a class="fn" title="return to article" href="#fnref"""+str(mark)+"""\">&#x21a9;</a>"""
    # Blank line
    else: 
        if (current == "<br />"):
            line = "<br />"
        else:
            line = line.strip()

    # Return the parsed line, now formatted with HTML.
    return line

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
    os.utime("Content/"+target, ((time.mktime(time.strptime(mod_time, "%Y/%m/%d %H:%M:%S"))), (time.mktime(time.strptime(mod_time, "%Y/%m/%d %H:%M:%S")))))

    # Return the read article type, for debugging.
    return article_type

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
    argv = sys.argv
    argc = len(argv)
    if (argc > 1):
        Interface(argv[1:])

    t1 = datetime.datetime.now()
    import cProfile
    Init()
    GenStatic()
    GenBlog()
    # cProfile.run("Init()")
    # cProfile.run("GenStatic()")
    # cProfile.run("GenBlog()")

    t2 = datetime.datetime.now()

    print ("Execution time: %s" % (t2-t1))