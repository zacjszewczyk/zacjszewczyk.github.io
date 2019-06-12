#!/usr/local/Cellar/python/3.7.3/bin/python3

import re

class Markdown:
    # Init

    def parseInlineMD(self, ln):
        line = ln.rstrip('\n')
        
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
            if (line[0] == "*" and line[1] == " "):
                line = "*"+line[1:].replace("*", "<em>", 1).replace("*", "</em>", 1)
                break
            line = line.replace("*", "<em>", 1).replace("*", "</em>", 1)

        ## Parse inline code
        while ("`" in line):
            line = line.replace("`", "<pre>", 1).replace("`", "</pre>", 1)

        ## Parse single quotatin marks
        line = line.replace(" '", " &#8216;").replace("' ", "&#8217; ")

        ## Parse aposrophes
        line = line.replace("'", "&#39;")

        ## Parse double quotation marks
        line = line.replace(' "', " &#8220;").replace('" ', "&#8221; ")

        ## Parse links
        for each in re.findall("\[([^\]]+)\]\(([^\)]+)\)", line):
            line = line.replace("["+each[0]+"]("+each[1]+")", "<a href=\""+each[1]+"\">"+each[0]+"</a>")

        return line

    line_tracker = ["", "", ""]
    line_type_tracker = ["", "", ""]
    line_indent_tracker = [0, 0, 0]

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
            self.line_type_tracker.append("ul")
        elif (__line[0].isdigit() and __line[1] == ".") or (__line[0:2].isdigit() and __line[3] == "."):
            self.line_type_tracker.append("ol")
        else:
            self.line_type_tracker.append("p")

        self.trimTracker(self.line_type_tracker)


    def updateIndentTracker(self, __line):
        self.line_indent_tracker.append(len(__line) - len(__line.lstrip(' ')))

        self.trimTracker(self.line_indent_tracker)

    def html(self, line):
        # Remove trailing newline
        line = line.rstrip('\n')

        self.updateLineTracker(line)
        self.updateLineTypeTracker(line)
        self.updateIndentTracker(line)

        print(self.line_tracker)
        print(self.line_type_tracker)
        print(self.line_indent_tracker)
        print()

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

        return line