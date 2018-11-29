#!/usr/bin/env python

import os
import time
import datetime
import re

# Global variables
types = ["", "", ""]
active = ""
file_idx = 0
files = {}
months = {"01" : "January", "02" : "February", "03" : "March", "04" : "April", "05" : "May", "06" : "June", "07" : "July", "08" : "August", "09" : "September", "10" : "October", "11" : "November", "12" : "December"}

def GetFiles():
    global files
    return files

def BuildFromTemplate(target, title, bodyid):
    fd = open("Structure/system/template.htm", "r")
    # Create first half of structure file, up to the point where content is required.
    content = fd.read()
    content = content.split("<!--Divider-->")
    content.append(content[0])
    fd.close()

    fd = open("Structure/"+target, "w")
    fd.write(content[0].replace("{{ title }}", title).replace("{{ BODYID }}", bodyid))
    fd.close()

def CloseTemplateBuild(target):
    fd = open("Structure/system/template.htm", "r")
    content = fd.read()
    content = content.split("<!--Divider-->")
    fd.close()

    fd = open("Structure/"+target, "a")
    fd.write(content[1])
    fd.close()

# Init method responsible for clearing the blog template file, writing
# the necessary opening tags, and creating the file dictionary.
def Init():
    global file_idx, files
    file_idx = 0
    files = {}
    
    fd = open("Structure/system/template.htm", "r")
    # Create first half of structure file, up to the point where content is required.
    content = fd.read()
    content = content.split("<!--Divider-->")
    content.append(content[0])
    fd.close()

    BuildFromTemplate("archives.html", "Post Archives - ", "postarchives")
    BuildFromTemplate("blog.html", "Blog - ", "blog")
    
    fd = open("Static/Main_feed.xml", "w")
    fd.write("""\
<?xml version='1.0' encoding='ISO-8859-1' ?>
<rss version="2.0" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Zac J. Szewczyk</title>
    <link>http://zacjszewczyk.com/</link>
    <description></description>
    <language>en-us</language>
    <atom:link href="http://zacjszewczyk.com/rss" rel="self" type="application/rss+xml" />
    <lastBuildDate>%s EST</lastBuildDate>
    <ttl>5</ttl>
    <generator>First Crack</generator>\n""" % (datetime.datetime.now().strftime("%a, %d %b %Y %I:%M:%S")))
    fd.close()

    for each in os.listdir("Content"):
        if (each.endswith(".txt") == True):
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

# Terminate method responsible for writing the closing tags to the blog and archives
# template files. 
def Terminate():
    fd = open("Structure/system/template.htm", "r")
    content = fd.read()
    content = content.split("<!--Divider-->")
    fd.close()

    CloseTemplateBuild("archives.html")
    CloseTemplateBuild("blog.html")

    fd = open("Static/Main_feed.xml", "a")
    fd.write("""\n</channel>\n</rss>""")
    fd.close()

def GenStatic():
    fd = open("Structure/system/template.htm", "r")
    content = fd.read();
    content = content.split("<!--Divider-->")

    fd = open("Structure/home.html", "w").close()
    fd = open("Structure/home.html", "a")
    home_fd = open("Structure/system/home.html", "r")
    home = home_fd.read().split("<!-- DIVIDER -->")
    fd.write(content[0].replace("{{ title }}", "").replace("{{ BODYID }}", "home").replace("<!-- SHEETS -->", home[0]))
    fd.write(home[1])
    fd.write(content[1])
    fd.close()

    fd = open("Structure/projects.html", "w").close()
    fd = open("Structure/projects.html", "a")
    projects_fd = open("Structure/system/projects.html", "r")
    projects = projects_fd.read().split("<!-- DIVIDER -->")
    fd.write(content[0].replace("{{ title }}", "Projects - ").replace("{{ BODYID }}", "projects").replace("<!-- SCRIPTS -->", projects[0]))
    fd.write(projects[1])
    fd.write(content[1])
    fd.close()

    fd = open("Structure/system/error.html", "w").close()
    fd = open("Structure/system/error.html", "a")
    fd.write(content[0].replace("{{ title }}", "Error - ").replace("{{ BODYID }}", "error"))
    fd.write("<!-- DIVIDER -->")
    fd.write(content[1].replace("<!-- SCRIPTS BLOCK -->", """<script type="text/javascript">document.getElementById("content_section").innerHTML = "<article><h2 class=\\"article_title\\">Error: 404 Not Found</h2><p>The requested resource at <u>"+window.location.href+"</u> could not be found.</p></article>"</script>"""))
    fd.close()    

def Migrate(file_name, mod_time):
    file_descriptor = open("Content/"+file_name, "r")
    article_content = file_descriptor.readline()

    if (article_content.startswith("# [") == True):
        article_type = "linkpost"
        article_content = article_content.lstrip("# ").replace(") #", "")
        article_content = article_content.split("]")
        article_title = article_content[0].lstrip("[")
        article_url = article_content[1].lstrip("(").rstrip(")")
    else:
        article_type = "original"
        article_title = article_content.replace("# ", "").replace(" #", "")
        article_url = file_name.replace(".txt", "").replace(" ", "-").lower()
        article_content = file_descriptor.readline()

    article_content = file_descriptor.read()

    file_descriptor.close()
    file_descriptor = open("Content/"+file_name, "w")
    file_descriptor.write("""Type: %s\nTitle: %s\nLink: %s\nPubdate: %s\nAuthor: %s\n\n%s""" % (article_type, article_title.strip(), article_url.strip(), mod_time, "Zac Szewczyk", article_content.strip()))

    file_descriptor.close()
    os.utime("Content/"+file_name, ((time.mktime(time.strptime(mod_time, "%Y/%m/%d %H:%M:%S"))), (time.mktime(time.strptime(mod_time, "%Y/%m/%d %H:%M:%S")))))

    return article_type

def Markdown(line):
    global types, active

    start = 1

    # Use {} to enclose an article series reference. Enclosed text identifies the article series, in the form of a file that the parser
    # opens, reads, and inserts into the actual article.
    # If line starts with {}, open target file, and return the contents with a return statement. Skip the rest.

    if (line.startswith("#")):
        line = ("<h%d>"+line.replace("#", "").strip()+"</h%d>") % (line.split(" ")[0].count("#"), line.split(" ")[0].count("#"))+"\n"
        types.append("<h>,,</h>")
    elif (re.match("(\[>[0-9]+\])", line) != None):
        types.append("<div class=\"footnote\">,,</div>")
    elif (re.match(">|\s{4}", line) != None):
        if ((types[-1] == "<blockquote>,,</blockquote>") or (types[-2] == "<blockquote>,,</blockquote>") or (types[-3] == "<blockquote>,,</blockquote>") or (types[-1] == "<bqt>,,</bqt>") or (types[-2] == "<bqt>,,</bqt>") or (types[-3] == "<bqt>,,</bqt>")):
            types.append("<bqt>,,</bqt>")
        else:
            types.append("<blockquote>,,</blockquote>")
    elif (re.match("\*\s", line) != None):
        line = line.replace("* ", "")
        if ((types[-1] == "<ul>,,</ul>") or (types[-2] == "<ul>,,</ul>") or (types[-3] == "<ul>,,</ul>") or (types[-1] == "<li>,,</li>") or (types[-2] == "<li>,,</li>") or (types[-3] == "<li>,,</li>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ul>,,</ul>")
    elif (re.match("[0-9]+", line) != None):
        start = line.split(".")[0]
        line = re.sub("[0-9]+\.\s", "", line)
        if ((types[-1] == "<ol>,,</ol>") or (types[-2] == "<ol>,,</ol>") or (types[-3] == "<ol>,,</ol>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ol>,,</ol>")
    elif (re.match("[a-zA-Z_\[\*\"]", line) != None):
        types.append("<p>,,</p>")
    elif (re.match("<", line) != None or re.match("#", line) != None):
        types.append("RAW HTML")
    else:
        if (line.strip() == "" and types[-1] == "<blank>,,</blank>"):
            types.append("<br />")
        else:
            types.append("<blank>,,</blank>")

    if (len(types) == 4):
        types.pop(0)

    current = types[-1]
    second = types[-2]
    third = types[-3]

    if (current != "RAW HTML"):
        # line = line.replace("&", "&#38;")
        if (re.search("&[a-z]{4}\;", line) != None):
            pass
        elif (re.search("(\&)", line) != None):
            line = line.replace("&", "&#38;")

        if (re.match("---", line) != None): # Parse <hr /> elements
            line = line.replace("---", "<hr />")

        if (re.search("(--)", line)): # Parse emdashes
            line = line.replace("--", "&#160;&#8212;&#160;")

        for each in re.findall("([\s\<\>\\\*\/\[\-\(]+\"[\[\w\%\#\\*<\>]+)", line): # Parse double-quote quotations
            ftxt = each.replace("\"", "&#8220;", 1)
            line = line.replace(each, ftxt)
        for each in re.findall("([\)\w+\.]+\"[\s\)\]\<\>\.\*\-\,])", line):
            ftxt = each.replace("\"", "&#8221;", 1)
            line = line.replace(each, ftxt)

        for each in re.findall("(\w+'[\w+|\s+])", line): # Parse single-quote quotations
            ftxt = each.replace("\'", "&#8217;")
            line = line.replace(each, ftxt)
        for each in re.findall("([\s\(]'\w+)", line):
            ftxt = each.replace("\'", "&#8216;", 1)
            line = line.replace(each, ftxt)

        for each in re.findall("\*\*{1}[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\*\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("**", "<strong>", 1)
            ftxt = ftxt.replace("**", "</strong> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)            

        for each in re.findall("\*{1}[\w:\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]]+\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("*", "<em>", 1)
            ftxt = ftxt.replace("*", "</em> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)

        for each in re.findall("(\!\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]+\]\(['\(\)\#\;?\@\%\w\&:\,\./\~\s\"\!\#\=\+-]+\))", line): # Parse images
            desc = each.split("]")[0].lstrip("![")
            url = each.split("]")[1].split(" ")[0].lstrip("(")
            if (url.startswith("http://zacjszewczyk.com/")):
                # print url.split("/")[-1]
                url = """/Static/Images/%s""" % (url.split("/")[-1])
            alt = each.split("]")[1].split(" &#8220;")[1].rstrip("&#8221;)")
            line = line.replace(each, "<div class=\"image\"><img src=\""+url+"\" alt=\""+alt+"\" title=\""+desc+"\"></div>")

        # This needs some attention to work with the new URL scheme
        for each in re.findall("""(\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]*\])(\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12\s*)?\))""", line): # Parse links
            desc = each[0].lstrip("[").rstrip("]")
            url = each[1].lstrip("(").rstrip(")").replace("&", "&amp;").strip()

            if (not url.startswith("http://") and not url.startswith("https://")):
                if (not url.endswith(".txt")):
                    if (url.endswith(".htm")):
                        url = "/blog/"+url.replace(" ", "-").replace(".htm", "").lower()
                        # print url
                        # print desc
                    else:
                        # print ("http://"+url)
                        # print desc
                        pass
                else:
                    url = "/blog/"+url.replace(" ", "-").replace(".txt", "").lower()

            if (url.endswith(".txt") == True):
                url = url.replace(".txt", "").replace(" ", "-").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+url.replace(" ", "-")+"\">"+desc+"</a>")
            elif (url == ""):
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+desc.replace("<em>", "").replace("</em>", "").replace(" ", "-")+"\">"+desc+"</a>")
            else:
                line = line.replace(each[0]+each[1], "<a href=\""+url+"\">"+desc+"</a>")

        # Parse footnotes
        for each in re.findall("(\[\^[0-9]+\])", line):
            mark = each.lstrip("[^").rstrip("]")
            url = """<sup id="fnref"""+mark+""""><a href="#fn"""+mark+"""" rel="footnote">"""+mark+"""</a></sup>"""
            line = line.replace(each, url)

        # Parse single-line comments
        if (re.match("[/]{2}", line) != None):
            line = line.replace("//","<!--")+" -->"
    else:
        if (line.startswith("<iframe")):
            line = "<div class=\"iframe\">"+line+"</div>"
        else:
            line = "<blockquote>"+line+"</blockquote>"

    if (current == "<p>,,</p>"): # If a paragraph
        line = current.replace(",,", line.strip())
    elif (current == "<ul>,,</ul>"): # If an unordered list
        active = "</ul>"
        line = current.split(",,")[0].replace(">", "start='"+str(start)+"'>")+"\n<li>"+line.strip()+"</li>"
    elif (current == "<ol>,,</ol>"): # If an ordered list
        active = "</ol>"
        line = current.split(",,")[0]+"\n<li>"+line.strip()+"</li>"
    elif (current == "<li>,,</li>"): # If a list item
        line = current.replace(",,", line.strip())
    elif ((current != "<li>,,</li>") and ((second == "<li>,,</li>") or (second == "<ul>,,</ul>") or (second == "<ol>,,</ol>"))): # If an element following a list item
        line = line.strip()+active+"\n"
        active = ""
    elif (current == "<blockquote>,,</blockquote>"): # If a blockquote
        active = "</blockquote>"
        line = current.split(",,")[0]+"\n<p>"+line.strip()+"</p>"
    elif (current == "<bqt>,,</bqt>"): # If the continuation of a blockquote
        line = "<p>"+line.strip().replace("> ", "")+"</p>"
    elif ((current != "<bqt>,,</bqt>") and ((second == "<bqt>,,</bqt>") or (second == "<blockquote>,,</blockquote>"))): # If an element following a blockquote
        line = line.strip().replace("> ", "")+"</blockquote>\n"
        active = ""
    elif ((current == "<div class=\"footnote\">,,</div>")): # If a footnote
        active = "</div>"
        mark = int(line.split("]")[0].lstrip("[>"))
        line = line.split("]")[1]
        if (mark == 1): # If the first footnote
            line = current.split(",,")[0].replace("div ", "div id=\"fn"+str(mark)+"\" ")+"\n<p>"+line.strip()+"""</p><a class="fn" title="return to article" href="#fnref"""+str(mark)+"""">&#x21a9;</a>"""
        else: # If a later footnote
            line = "</div>"+current.split(",,")[0]+"<p>"+line.strip()+"</p>"
            line = line.replace("div ", "div id=\"fn"+str(mark)+"\" ")+"""<a class="fn" title="return to article" href="#fnref"""+str(mark)+"""\">&#x21a9;</a>"""
    else: # Blank line
        if (current == "<br />"):
            line = "<br />"
        else:
            line = line.strip()

    return line

def GenPage(source, timestamp):
    source_fd = open("Content/"+source, "r")

    line = source_fd.readline()
    if (line.startswith("Type:") == False):
        Migrate(source, timestamp)
    source_fd.close()
    source_fd = open("Content/"+source, "r")

    target_fd = open("Structure/"+source.lower().replace(" ", "-").replace(".txt", ".html"), "w").close()
    target_fd = open("Structure/"+source.lower().replace(" ", "-").replace(".txt", ".html"), "a")

    fd = open("Structure/system/template.htm", "r")
    content = fd.read();
    content = content.split("<!--Divider-->")
    fd.close()

    content[0] = content[0].replace("<!-- SCRIPTS -->", """\
            <script type="text/javascript">
                function insertAfter(e,a){a.parentNode.insertBefore(e,a.nextSibling)}for(var fn=document.getElementsByClassName("footnote"),i=0;i<fn.length;i++){var a=[].slice.call(fn[i].children);if("[object HTMLParagraphElement]"==a[a.length-1]){var temp=a[a.length-2];a[a.length-2]=a[a.length-1],a[a.length-1]=temp;for(var j=0;j<a.length;j++)fn[i].removeChild(a[j]);for(var j=0;j<a.length;j++)fn[i].appendChild(a[j])}}
                //https://www.dirtymarkup.com/, http://jscompress.com/
                if (document.title.search("Ipad")) {document.title = document.title.replace("Ipad", "iPad")}
            </script>""").replace("{{ BODYID }}", "post")
    
    idx = 0
    title = ""

    for line in iter(source_fd.readline, ""):
        if (idx == 0):
            title += "<article>\n    <h2 class=\"article_title\">\n        <a href=\"{{URL}}\" class=\"%s\">{{URL_TITLE}}</a>" % (line.replace("Type: ", "").strip())
        elif (idx == 1):
            title = title.replace("{{URL_TITLE}}", line.replace("Title: ", "").strip())
            content[0] = content[0].replace("{{ title }}", line.replace("Title: ", "").strip()+" - ")
        elif (idx == 2):
            line = line.replace("Link: ", "").strip()
            if (not line.startswith("http") and line.endswith(".htm")):
                line = line.replace(".htm", "").replace(" ", "-").lower()
            title = title.replace("{{URL}}", line)+"\n    </h2>"
        elif (idx == 3):
            # print line
            line = line.replace("Pubdate: ", "").replace(" ", "/").split("/")
            title += """\n    <time datetime="%s-%s-%s" pubdate="pubdate">By <link rel="author">Zac J. Szewczyk</link> on <a href="%s">%s</a>/<a href="%s">%s</a>/%s %s</time>""" % (line[0], line[1], line[2], "/blog/"+line[0], line[0], "/blog/"+line[0]+"/"+line[1], line[1], line[2], line[3])
        elif (idx == 4):
            target_fd.write(content[0])
            target_fd.write(title.strip()+"\n")
        elif (idx > 4):
            target_fd.write("\n    "+Markdown(line))

        idx += 1
    else:
        target_fd.write("\n</div>\n</article>")
        # target_fd.write("\n{% endblock %}")
        target_fd.write(content[1])
        
    target_fd.close()
    source_fd.close()

def AppendContentOfXToY(target, source):
    source_fd = open("Content/"+source, "r")
    target_fd = open("Structure/"+target+".html", "a")

    ptype = "linkpost"
    idx = 0
    title = ""

    for line in iter(source_fd.readline, ""):
        if (idx == 0):
            if (line.startswith("Type:") == False):
                ptype = Migrate(source, mod_time).strip()
            else:
                ptype = line.replace("Type: ", "").strip()

            title += "<article>\n    <h2 class=\"article_title\">\n        <a href=\"{{URL}}\" class=\"%s\">{{URL_TITLE}}</a>" % (line.replace("Type: ", "").strip())
        elif (idx == 1):
            title = title.replace("{{URL_TITLE}}", line.replace("Title: ", "").strip())
        elif (idx == 2):
            title = (title.replace("{{URL}}", "/blog/"+source.lower().replace(" ", "-").replace(".txt", "")), title.replace("{{URL}}", line.replace("Link: ", "").strip()))[ptype == "linkpost"]+"\n    </h2>"
            url = (("/blog/"+source.lower().replace(" ", "-").replace(".txt", "")), title.replace("{{URL}}", line.replace("Link: ", "").strip()))[ptype == "linkpost"]
        elif (idx == 3):
            line = line.replace("Pubdate: ", "").replace(" ", "/").split("/")
            title += """\n    <time datetime="%s-%s-%s" pubdate="pubdate">By <link rel="author">Zac J. Szewczyk</link> on <a href="%s">%s</a>/<a href="%s">%s</a>/%s %s</time>""" % (line[0], line[1], line[2], "/blog/"+line[0], line[0], "/blog/"+line[0]+"/"+line[1], line[1], line[2], line[3])
        elif (idx == 4):
            target_fd.write(title.strip()+"\n")
        elif (idx == 6):
            target_fd.write("\n    "+Markdown(line).replace("#fn", url+"#fn"))
        elif (idx > 6 and ptype == "linkpost"):
            target_fd.write("\n    "+Markdown(line).replace("#fn", url+"#fn"))

        idx += 1
    else:
        target_fd.write("\n    <p class=\"read_more_paragraph\">\n        <a class=\"read_more_link\" href=\"/blog/%s\">&#x24CF;</a>\n    </p>" % (source.lower().replace(" ", "-").replace(".txt", "")))
        target_fd.write("\n</article>\n")

    target_fd.close()
    source_fd.close()

def AppendToFeed(source):
    source_fd = open("Content/"+source, "r")
    feed_fd = open("Static/Main_feed.xml", "a")

    ptype = "linkpost"
    idx = 0

    feed_fd.write("        <item>\n")

    for line in iter(source_fd.readline, ""):
        if (line.find("&")):
            line = line.replace("&", "&#38;")
        if (idx == 0):
            ptype = line.replace("Type: ", "").strip()
        elif (idx == 1):
            feed_fd.write("            <title>"+line.replace("Title: ", "").strip()+"</title>\n")
        elif (idx == 2):
            if (ptype == "linkpost"):
                if (not line.startswith("http://")):
                    line = "http://"+line
                feed_fd.write("            <link>"+line.replace("Link: ", "").strip()+"</link>\n")
                feed_fd.write("            <guid>"+line.replace("Link: ", "").strip()+"</guid>\n")
            else:
                feed_fd.write("            <link>http://zacjszewczyk.com/blog/"+source.lower().replace(" ", "-").replace(".txt", "").lower()+"</link>\n")
                feed_fd.write("            <guid>http://zacjszewczyk.com/blog/"+source.lower().replace(" ", "-").replace(".txt", "").lower()+"</guid>\n")
        elif (idx == 3):
            feed_fd.write("            <description>")
        elif (idx == 6):
            feed_fd.write("\n                "+Markdown(line).replace("&", "&#38;").replace("<", "&lt;").replace(">", "&gt;"))

        elif (idx > 6 and ptype == "linkpost"):
            feed_fd.write("\n                "+Markdown(line).replace("&", "&#38;").replace("<", "&lt;").replace(">", "&gt;"))
        
        idx += 1

    else:
        feed_fd.write("\n            </description>\n        </item>\n")

    feed_fd.close()
    source_fd.close()

def GetTitle(source):
    fd = open("Content/"+source, "r")
    fd.readline()
    title = fd.readline().replace("Title: ", "")
    fd.close()
    return title

def RegenBlog():
    global files
    global file_idx
    Init()

    fd = open("Structure/system/template.htm", "r")
    content = fd.read();
    content = content.split("<!--Divider-->")
    fd.close()

    for year in sorted(files, reverse=True):
        year_fd = open("Structure/"+year+".html", "w").close()
        year_fd = open("Structure/"+year+".html", "a")
        year_fd.write(content[0].replace("{{ title }}", "Post Archives - ").replace("{{ BODYID }}", "archives"))
        year_fd.write("""<table id="big_table">""")
        year_fd.write("    <tr>\n        <td>%s</td>\n    </tr>\n" % (year))
        for month in sorted(files[year], reverse=True):
            year_fd.write("    <tr>\n        <td><a href=\"%s\">%s</a></td>\n    </tr>\n" % ("/blog/"+year+"/"+month, months[month]))
            month_fd = open("Structure/"+year+"-"+month+".html", "w").close()
            month_fd = open("Structure/"+year+"-"+month+".html", "a")
            month_fd.write(content[0].replace("{{ title }}", "Post Archives - ").replace("{{ BODYID }}", "archives").replace("<!--BLOCK HEADER-->", "<article>\n<p>\n"+months[month]+", <a href=\"/blog/"+year+"\">"+year+"</a>\n</p>\n</article>"))
            for day in sorted(files[year][month], reverse=True):
                for timestamp in sorted(files[year][month][day], reverse=True):
                    month_fd.write("<article>\n    %s<a href=\"%s\">%s</a>\n</article>\n" % (year+"/"+month+"/"+day+" "+timestamp+": ", "/blog/"+files[year][month][day][timestamp].lower().replace(" ", "-").replace(".txt", ""), GetTitle(files[year][month][day][timestamp])))
                    GenPage(files[year][month][day][timestamp], "%s/%s/%s %s" % (year, month, day, timestamp))
                    if (file_idx < 25):
                        AppendContentOfXToY("blog", files[year][month][day][timestamp])
                    elif (file_idx == 25):
                        buff = """\n<article>\n<table id="big_table">\n    <tr>\n"""
                        for each in sorted(files, reverse=True)[:3]:
                            buff += """\n        <td>\n            <a href=\"/blog/%s\">%s</a>\n        </td>""" % (each.lower(), each)
                        buff += """\n    </tr>\n    <tr>\n"""
                        for each in sorted(files, reverse=True)[3:]:
                            buff += """\n        <td>\n            <a href=\"/blog/%s\">%s</a>\n        </td>""" % (each.lower(), each)
                        buff += """\n    </tr>\n</table>\n</article>\n"""
                        archives_fd = open("Structure/archives.html", "a")
                        archives_fd.write(buff)
                        archives_fd.close()
                        AppendContentOfXToY("archives", files[year][month][day][timestamp])
                    else:
                        AppendContentOfXToY("archives", files[year][month][day][timestamp])
                    AppendToFeed(files[year][month][day][timestamp])
                    file_idx += 1
            month_fd.write(content[1])
            month_fd.close()
        year_fd.write("</table>\n"+content[1])
        year_fd.close()

    Terminate()

if __name__ == '__main__':
    t1 = datetime.datetime.now()
    GenStatic()
    RegenBlog()
    t2 = datetime.datetime.now()

    print ("Execution time: %s" % (t2-t1))