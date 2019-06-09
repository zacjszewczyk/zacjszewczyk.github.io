#!/usr/local/Cellar/python/3.7.3/bin/python3

import re

class Markdown:
    __url = ""
    __raw = ""
    __html = ""
    __tracker = ["", "", ""]
    __state = ""

    __delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())

    def __init__(self, url=""):
        if (url == ""):
            from sys import exit
            print("Error: no base URL given.")
            exit(1)
        self.__url = url

    def raw(self):
        return self.__raw

    # Changes to the Markdown processor
    # 1. Do not do any processing on blank lines or raw HTML. This seems like
    # an obvious optimization step, but it was one I overlooked previously.
    # Even though the "if" statements and regular expressions would eventually
    # determine that no work was necessary on lines line these, those checks
    # take time. I have now eliminated that wasted time.
    # 2. Just execute simple parsing operations. I used to check for emdashes
    # before processing them, which wastes time for such a simple operation.
    # Just executing the replacement takes about 75% of the time.
    def html(self, line):
        # line = line.strip()
        
        self.__raw = line
        
        # Skip over all the processing if we're just looking at a blank line or
        # raw HTML.
        if (line == '\n'):
            self.__updateTracker("blank")
            self.__raw = ""
            self.__html = line.strip()

            if (self.__tracker[-2] in ["ul", "li"]):
                self.__html = "</ul>\n"+self.__html

            return self.__html
        elif (line[0] == "<"):
            self.__updateTracker("raw")
            line = line.strip()
            self.__raw = line
            self.__html = line
            return self.__html

        # Determine type of line
        ## Unordered list
        ### Unordered lists first, to capture lines that start with '* ', '+ ',
        ### and '- '. These could also start paragraphs, if there is no
        ### succeeding space, so check for these chars with a space first.
        if (line[0:2] in ['* ', '+ ', '- ']):
            if (self.__tracker[-1] in ["ul", "li"]):
                self.__updateTracker("li")
            else:
                self.__updateTracker("ul")
        ## Paragraph
        ### Paragraphs second. These can start with letters, or--in the case of
        ### italics or bold--one or more '*' or '_' not followed by a space,
        ### which would have been captured above as an unordered list.
        elif (line[0].isalpha() or line[0] in ['*', '_']):
            self.__updateTracker("p")
        ## Header
        elif (line[0] == '#'):
            self.__updateTracker("header")
        # Catch an unknown line type
        else:
            self.__updateTracker("UNKNOWN")

        line = line.strip()

        # Block parsing. Parse based on type of line
        ## Paragraph
        if (self.__tracker[-1] == "p"):
            line = "<p>"+line+"</p>"
            
        ## Unordered list 
        elif (self.__tracker[-1] == "ul"):
            line = "<ul>\n    <li>"+line[2:]+"</li>"
        elif (self.__tracker[-1] == "li"):
            line = "    <li>"+line[2:]+"</li>"
        
        ## Header
        elif (self.__tracker[-1] == "header"):
            l = len(line) - len(line.lstrip("#"))
            line = "<h"+str(l)+" id=\""+''.join(ch for ch in line if ch.isalnum())+"\">"+line.lstrip("#").rstrip("#").strip()+"<h"+str(l)+">"

        # Generic parsing
        line = line.replace("---", "<hr />")

        ## Escape ampersands. Replace them with the appropriate HTML entity.
        line = line.replace("&", "&#38;")

        ## Parse emdashes
        line = line.replace("--", "&#160;&#8212;&#160;")

        ## Parse escaped asteriscs, to keep them from being interpreted as
        ## asterics indicating bold or italic text.
        line = line.replace("\*", "&#42;")

        ## Prase **, or <strong> tags, first, to keep them from being
        ## interpreted as <em> tags...
        while ("**" in line):
            line = line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)

        ## ... then parse the remaining <em> tags
        while ("*" in line):
            line = line.replace("*", "<em>", 1).replace("*", "</em>", 1)

        ## Parse inline code
        while ("`" in line):
            line = line.replace("`", "<pre>", 1).replace("`", "</pre>", 1)

        ## Parse single quotatin marks
        line = line.replace(" '", " &#8216;").replace("' ", "&#8217; ")

        ## Parse double quotation marks
        line = line.replace(' "', " &#8220;").replace('" ', "&#8221; ")

        ## Parse links
        for each in re.findall("\[([^\]]+)\]\(([^\)]+)\)", line):
            line = line.replace("["+each[0]+"]("+each[1]+")", "<a href=\""+each[1]+"\">"+each[0]+"</a>")

        print("    "+str(self.__tracker))
        self.__html = line
        return self.__html

    # Internal methods
    def __updateTracker(self, n):
        self.__tracker.append(str(n))
        if (len(self.__tracker) > 3):
            self.__tracker.pop(0)

    # Debug methods
    def getStats(self):
        return "base_url",self.__url