#!/usr/local/Cellar/python/3.7.3/bin/python3

import re

class Markdown:
    # Init

    def parseInlineMD(self, __line):
        __line = __line.rstrip('\n')
        
        # Generic parsing
        __line = __line.replace("---", "<hr />")

        ## Escape ampersands. Replace them with the appropriate HTML entity.
        __line = __line.replace("&", "&#38;")

        ## Parse emdashes
        __line = __line.replace("--", "&#160;&#8212;&#160;")

        ## Parse escaped asteriscs, to keep them from being interpreted as
        ## asterics indicating bold or italic text.
        __line = __line.replace("\*", "&#42;")

        ## Prase **, or <strong> tags, first, to keep them from being
        ## interpreted as <em> tags...
        while ("**" in __line):
            __line = __line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)

        ## ... then parse the remaining <em> tags
        while ("*" in __line):
            if (__line[0] == "*" and __line[1] == " "):
                __line = "*"+__line[1:].replace("*", "<em>", 1).replace("*", "</em>", 1)
                break
            __line = __line.replace("*", "<em>", 1).replace("*", "</em>", 1)

        ## Parse in__line code
        while ("`" in __line):
            __line = __line.replace("`", "<pre>", 1).replace("`", "</pre>", 1)

        ## Parse single quotatin marks
        __line = __line.replace(" '", " &#8216;").replace("' ", "&#8217; ")

        ## Parse aposrophes
        __line = __line.replace("'", "&#39;")

        ## Parse double quotation marks
        __line = __line.replace(' "', " &#8220;").replace('" ', "&#8221; ")

        ## Parse links
        for each in re.findall("\[([^\]]+)\]\(([^\)]+)\)", __line):
            __line = __line.replace("["+each[0]+"]("+each[1]+")", "<a href=\""+each[1]+"\">"+each[0]+"</a>")

        return __line

    line_tracker = ["", "", ""]
    line_type_tracker = ["", "", ""]
    line_indent_tracker = [0, 0, 0]
    
    opening_map = {"ul" : "<ul>", "li" : "<li>"}
    closing_map = {"ul" : "</ul>", "li" : "</li>"}

    unordered_list = ["*", "+", "-"]

    close_out = []

    def getLineType(self, __pos):
        return self.line_type_tracker[__pos]

    def trimTracker(self, __trkr):
        if (len(__trkr) > 3):
            __trkr.pop(0)

    def updateLineTracker(self, __line):
        self.line_tracker.append(__line)
        self.trimTracker(self.line_tracker)

    def updateLineTypeTracker(self, __line):
        __line = __line.lstrip(' ')

        if (len(__line) == 0):
            self.line_type_tracker.append("blank")
        elif (__line[0] == "#"):
            self.line_type_tracker.append("header")
        elif (__line[0:4] == "---"):
            self.line_type_tracker.append("hr")
        elif (__line[0:2] == "!["):
            self.line_type_tracker.append("img")
        elif (__line[0] == "{"):
            self.line_type_tracker.append("idx")
        elif (__line[0] in ['*', '+', '-'] and __line[1] == ' '):
            if (self.queryIndentTracker(-1) > self.queryIndentTracker(-2)):
                self.line_type_tracker.append("ul")
            elif (self.queryIndentTracker(-1) < self.queryIndentTracker(-2)):
                self.line_type_tracker.append("/ul")
            elif (self.line_type_tracker[-1] == "ul" or self.line_type_tracker[-1] == "li"):
                self.line_type_tracker.append("li")
            elif (self.line_type_tracker[-1] == "/ul" and len(self.close_out) != 0):
                self.line_type_tracker.append("li")
            else:
                self.line_type_tracker.append("ul")
        elif (__line[0].isdigit() and __line[1] == ".") or (__line[0:2].isdigit() and __line[3] == "."):
            self.line_type_tracker.append("ol")
        else:
            self.line_type_tracker.append("p")

        self.trimTracker(self.line_type_tracker)

    def updateIndentTracker(self, __line):
        self.line_indent_tracker.append(len(__line) - len(__line.lstrip(' ')))

        self.trimTracker(self.line_indent_tracker)

    def queryIndentTracker(self, __pos):
        return self.line_indent_tracker[__pos]

    def closeOut(self):
        print(self.close_out)
        return '\n'.join(self.close_out)

    def html(self, __line):
        # Remove trailing newline
        __line = __line.rstrip('\n')

        self.updateIndentTracker(__line)
        self.updateLineTracker(__line)
        self.updateLineTypeTracker(__line)

        print(self.line_tracker)
        print(self.line_type_tracker)
        print(self.line_indent_tracker)
        print()

        __line = __line.lstrip(' ')
        if (len(__line) == 0):
            __line = self.closeOut()
            self.close_out = []
            return __line

        if (self.getLineType(-1) == "ul"):
            __line = "<ul>"+'\n'+"    <li>"+__line[2:]+"</li>"
            self.close_out.append("</ul>")
        elif (self.getLineType(-1) == "li"):
            __line = "    <li>"+__line[2:]+"</li>"
        elif (self.getLineType(-1) == "/ul"):
            __line = "</ul>\n<li>"+__line[2:]+"</li>"
            self.close_out.remove("</ul>")


        # if (self.getLineType(-1) in ["ul", "ol"]):
        #     if (self.getLineType(-2) in ["ul", "ol"]):
        #         __line = "<li>"+__line.split('\n')[-1][2:]+"</li>"
        #     else:
        #         __line = self.opening_map[self.getLineType(-1)]+'\n'+"<li>"+__line[2:]+"</li>"

        # # Remove trailing newline
        # line = line.rstrip('\n')
        
        # print("OLD: '%s'" % line)

        # # Handle blank lines
        # if (len(line) == 0):
        #     self.updateTracker("blank")
        #     line = self.closing_tags
        #     print("'%s'" % line)
        #     self.closing_tags = ""
        #     return line

        # # Handle headers
        # if (line[0] == "#"):
        #     l = len(line) - len(line.lstrip("#"))
        #     line = "<h"+str(l)+" id=\""+''.join(ch for ch in line if ch.isalnum())+"\">"+line.lstrip("#").rstrip("#").strip()+"<h"+str(l)+">"
        #     self.updateTracker("hx")
        # # Handle horizontal rules
        # elif (line[0:4] == "---"):
        #     line = "<hr />"
        #     self.updateTracker("hr")
        # # Handle images
        # elif (line[0:2] == "!["):
        #     line = line.split("]")
        #     desc = line[0][2:]
        #     url = line[1].split(" ")[0][1:]
        #     alt = line[1].split(" ")[1][1:-2]
        #     line = "<div class='image'><img src='%s' alt='%s' title='%s' /></div>" % (url, alt, desc)
        #     self.updateTracker("img")
        # # Handle series index
        # elif (line[0] == "{"):
        #     with open("./Content/System/"+line[1:-1], "r") as fd:
        #         line = "<ul style=\"border:1px dashed gray\" id=\"series_index\">\n"
        #         for each in fd:
        #             line += "    <li>"+each.strip()+"</li>\n"
        #         line += "</ul>"
        #     self.updateTracker("si")

        # # Parse multi-line block-level elements
        # ## Unordered list
        # if (self.indent_level < (len(line) - len(line.lstrip(' ')))):
        #     print("Sub-element")
        #     print("Current: %d" % self.indent_level)
        #     print("New: %d" % (len(line) - len(line.lstrip(' '))))
        #     self.indent_level = (len(line) - len(line.lstrip(' ')))
        #     # line = self.opening_map[self.getLineType(line)]+'\n'+line
        #     self.tracker[-1] = "" # This is the problem line ... ?
        # elif (self.indent_level > (len(line) - len(line.lstrip(' ')))):
        #     print("Exiting sub-element")
        #     print("Current: %d" % self.indent_level)
        #     print("New: %d" % (len(line) - len(line.lstrip(' '))))
        #     self.indent_level = (len(line) - len(line.lstrip(' ')))
        #     line = self.closing_map[self.getLineType(self.tracker[-1])]+'\n'+"<li>"+line[2:]+"</li>"

        # if (self.getLineType(line) == "ul"):
        #     if (self.tracker[-1] != "ul"):
        #         line = "<ul>\n    <li>"+line[2:]+"</li>"
        #         self.closing_tags = "</ul>"
        #     else:
        #         line = "<li>"+line[2:]+"</li>"
        #     self.updateTracker("ul")

        # if (self.tracker[-1] == ''):
        #     self.updateTracker("ERROR w/ %s" % line)
            
        # # This should be done after block-level parsing. Done as part of block-level parsing,
        # # where appropriate, and then finally when wrapping in <p> tags if nowhere else.
        # # # Treat as a paragraph. Parse inline MarkDown
        # # line = self.parseInlineMD(line)

        # print("NEW: '%s'" % line)
        # print ("TRACKER: "+str(self.tracker))

        return __line