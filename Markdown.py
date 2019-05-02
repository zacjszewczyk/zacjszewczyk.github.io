#!/usr/bin/python

from re import findall, search, sub, match, search # Import re functions
from os import chdir # Import chdir to locate content files

# Global variables for pasring Markdown
# - types: Keeps track of current and previous two line types
# - active: The corresponding closing tag for the active block-level element
types = ["", "", ""]
active = ""
pre = False

# Tell Proofer where it can find the content files
path_to_content_files = "/Users/zjszewczyk/Dropbox/Code/Standalone/"

# Method: Markdown
# Purpose: Take a raw string from a file, formatted in Markdown, and parse it into HTML.
# Parameters:
# - Line: Line to be parsed. (String)
def Markdown(line):
    # Make global variables accessible in the method, and initialize method variables.
    # Must be global to persist between method calls.
    global types, active, pre
    start = 1

    # Use {} to enclose an article series reference. Enclosed text identifies the article series, in the form of a file that the parser
    # opens, reads, and inserts into the actual article.
    # If line starts with {}, open target file, and return the contents with a return statement. Skip the rest w/ a return statement.

    if (pre == True):
        types.append("RAW HTML")
    # Part of a series
    elif (line[0] == "{"):
        line = line.strip()
        chdir(path_to_content_files)
        fd = open("Content/System/"+line[1:-1], "r")
        line = "<ul style=\"border:1px dashed gray\" id=\"series_index\">\n"
        for each in fd.read().split("\n"):
            line += "    <li>"+Markdown(each)+"</li>\n"
        line += "</ul>"
        types.append("RAW HTML")
        fd.close()
    # Header elements, <h1>-<h6>
    elif (line[0] == "#"):
        line = line.split("[")[0].strip()
        header_id = sub('\W+','', line.title()).strip()
        line = ("<h%d class=~headers~ id=~%s~>"+line.replace("#", "").strip()+"<span>&nbsp;<a href=~#%s~>#</a></span></h%d>") % (line.split(" ")[0].count("#"), header_id, header_id, line.split(" ")[0].count("#"))+"\n"
        types.append("<h>,,</h>")
    # Images
    elif (line[0:1] == "!["):
        types.append("<img>,,</img>")
    # Footnote
    elif (match("(\[>[0-9]+\])", line) != None):
        types.append("<div class=\"footnote\">,,</div>")
    # Blockquotes
    elif (match(">|\s{4}", line) != None):
        if ((types[-1] == "<blockquote>,,</blockquote>") or (types[-1] == "<bqt>,,</bqt>")):
            types.append("<bqt>,,</bqt>")
        else:
            types.append("<blockquote>,,</blockquote>")
    # Unordered lists
    elif (match("\*\s", line) != None):
        line = line.replace("* ", "")
        if ((types[-1] == "<ul>,,</ul>") or (types[-2] == "<ul>,,</ul>") or (types[-3] == "<ul>,,</ul>") or (types[-1] == "<li>,,</li>") or (types[-2] == "<li>,,</li>") or (types[-3] == "<li>,,</li>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ul>,,</ul>")
    # Ordered lists
    elif (match("[0-9]+", line) != None):
        start = line.split(".")[0]
        line = sub("[0-9]+\.\s", "", line)
        if ((types[-1] == "<ol>,,</ol>") or (types[-2] == "<ol>,,</ol>") or (types[-3] == "<ol>,,</ol>")):
            types.append("<li>,,</li>")
        else:
            types.append("<ol>,,</ol>")
    # Paragraphs
    elif (match("[a-zA-Z_\[\*\"]", line) != None):
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
        if (search("&[a-z]{4}\;", line) != None):
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
        for each in findall("([\s\<\>\\\*\/\[\-\(]+\"[\[\w\%\#\\*<\>]+)", line):
            ftxt = each.replace("\"", "&#8220;", 1)
            line = line.replace(each, ftxt)
        for each in findall("([\)\w+\.]+\"[\s\)\]\<\>\.\*\-\,])", line):
            ftxt = each.replace("\"", "&#8221;", 1)
            line = line.replace(each, ftxt)
        # Parse single-quote quotations
        for each in findall("(\w+'[\w+|\s+])", line):
            ftxt = each.replace("\'", "&#8217;")
            line = line.replace(each, ftxt)
        for each in findall("([\s\(]'\w+)", line):
            ftxt = each.replace("\'", "&#8216;", 1)
            line = line.replace(each, ftxt)
        # Interpret inline code
        for each in findall(r"\%[\w:\/\"\.\+'\s\.|#\\&=,\$\!\?\;\-\[\]\/<>]+\%", line):
            if (len(each.split(" ")) > 7):
                continue
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = ftxt.replace("%", "<span class='command'>", 1)
            ftxt = ftxt.replace("%", "</span> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)
            line = line.replace("&#8217;", "'").replace("&#8216;", "'").replace("&#8221;", '"').replace("&#8220;", '"')
        # Interpret <strong> tags
        for each in findall("\*\*{1}[\w:\"\.\+'\s\.|\(\)#/\\\>\<&=,\$\!\?\;\-\[\]]+\*\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("**", "<strong>", 1)
            ftxt = ftxt.replace("**", "</strong> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)            
        # Interpret <em> tags
        for each in findall("\*{1}[\w:\"\.\+'\s\.|\(\)#/\\\>\<&=,\$\!\?\;\-\[\]]+\*{1}", line):
            ftxt = each
            line = line.replace(each, "&&TK&&")
            ftxt = each.replace("*", "<em>", 1)
            ftxt = ftxt.replace("*", "</em> ", 1).strip()
            line = line.replace("&&TK&&", ftxt)
        # Parse images, both local and remote
        for each in findall("(\!\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]+\]\(['\(\)\#\;?\@\%\w\&:\,\./\~\s\"\!\#\=\+-]+\))", line):
            desc = each.split("]")[0][2:]
            url = each.split("]")[1].split(" ")[0][1:]
            if (url.startswith("http://zacjszewczyk.com/")):
                # print url.split("/")[-1]
                url = """/assets/Images/%s""" % (url.split("/")[-1])
            alt = each.split("]")[1].split(" &#8220;")[1].rstrip("&#8221;)")
            line = line.replace(each, "<div class=\"image\"><img src=\""+url+"\" alt=\""+alt+"\" title=\""+desc+"\"></div>")
        # This needs some attention to work with the new URL scheme
        # Parse links, both local and remote
        for each in findall("""(\[[\w\@\s\"'\|\<\>\.\#?\*\;\%\+\=!\,-:$&]*\])(\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12\s*)?\))""", line):
            desc = each[0][1:-1]
            url = each[1][1:-1].replace("&", "&amp;").strip()
            
            if ("http://" != url[0:7] and "https://" != url[0:8]):
                if (".txt" != url[-4:]):
                    if (".htm" == url[-4:]):
                        url = ""+url.replace(" ", "-").lower()
                else:
                    url = "http://zacs.site/blog/"+url.replace(" ", "-").replace(".txt", ".html").lower()

            if (".txt" == url[-4:]):
                url = url.replace(".txt", "").replace(" ", "-").replace("&#8220;", "").replace("&#8221;", "").replace("&#8217;", "").replace("&#8216;", "").replace("&#8217;", "")
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+url.replace(" ", "-")+"\">"+desc+"</a>")
            elif (url == ""):
                line = line.replace(each[0]+each[1], "<a class=\"local\" href=\""+desc.replace("<em>", "").replace("</em>", "").replace(" ", "-")+"\">"+desc+"</a>")
            else:
                line = line.replace(each[0]+each[1], "<a href=\""+url+"\">"+desc+"</a>")
        # Parse footnotes
        for each in findall("(\[\^[0-9]+\])", line):
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
            if (line.find("</pre>") == -1):
                pre = True
        elif (pre == True):
            if (line.find("</pre>") != -1):
                pre = False
            return line.strip()
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

    line = line.replace("~", "'")

    # Return the parsed line, now formatted with HTML.
    return line