#!/usr/local/bin/python3

# Import methods
from re import findall # re.findall, for links

class Markdown:
    # Init

    # Method: parseInlineMD
    # Purpose: Turn all inline MD tags into HTML.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line to process, mangled (String)
    # Return:
    # - Parsed line (String)
    def parseInlineMD(self, __line):
        __line = __line.rstrip('\n')
        
        # Generic parsing
        __line = __line.replace("---", "<hr />")

        ## Parse emdashes
        __line = __line.replace("--", "&#160;&#8212;&#160;")

        ## Prase **, or <strong> tags, first, to keep them from being
        ## interpreted as <em> tags...
        while ("**" in __line):
            __line = __line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)

        ## ... then parse the remaining <em> tags
        if (__line.count("*") % 2 == 0):
            while ("*" in __line):
                if (__line[0] == "*" and __line[1] == " "):
                    __line = "*"+__line[1:].replace("*", "<em>", 1).replace("*", "</em>", 1)
                    break
                __line = __line.replace("*", "<em>", 1).replace("*", "</em>", 1)

        ## Parse in__line code
        while ("`" in __line):
            __line = __line.replace("`", "<code>", 1).replace("`", "</code>", 1)

        ## Parse single quotatin marks
        __line = __line.replace(" '", " &#8216;").replace("' ", "&#8217; ")

        ## Parse aposrophes
        __line = __line.replace("'", "&#39;")

        ## Parse double quotation marks
        __line = __line.replace(' "', " &#8220;").replace('" ', "&#8221; ")

        ## Parse links
        for each in findall("\[([^\]]+)\]\(([^\)]+)\)", __line):
            __line = __line.replace("["+each[0]+"]("+each[1]+")", "<a href=\""+each[1]+"\">"+each[0]+"</a>")

        return __line

    line_tracker = ["", "", ""]
    line_type_tracker = ["", "", ""]
    line_indent_tracker = [0, 0, 0]
    
    opening_map = {"ul" : "<ul>", "li" : "<li>"}
    closing_map = {"ul" : "</ul>", "li" : "</li>"}

    unordered_list = ["*", "+", "-"]

    close_out = []
    pre = False

    # Method: getLineType
    # Purpose: Return the type of line for the specified position.
    # Parameters:
    # - self: Class namespace
    # - __pos: Desired position, mangled.
    # Return:
    # - Type of line at specified position (String)
    def getLineType(self, __pos):
        return self.line_type_tracker[__pos]

    # Method: trimTracker
    # Purpose: Keep tracker lists to a max of three elements.
    # Parameters:
    # - self: Class namespace
    # - __trkr: Reference to tracker to be trimmed.
    # Return: None.
    def trimTracker(self, __trkr):
        if (len(__trkr) > 3):
            __trkr.pop(0)

    # Method: updateLineTracker
    # Purpose: Keep track of raw lines.
    # Parameters:
    # - self: Class namespace
    # - __line: Raw Markdown line, mangled.
    # Return: None.
    def updateLineTracker(self, __line):
        self.line_tracker.append(__line)
        self.trimTracker(self.line_tracker)

    # Method: updateLineTypeTracker
    # Purpose: Determine type of line, and whether it is part of a larger
    # block-level element, and annotate that in the line type tracker.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line to process, mangled. (String)
    # Return: None.
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
            elif (len(self.close_out) != 0):
                self.line_type_tracker.append("li")
            else:
                self.line_type_tracker.append("ul")
        elif (__line[0].isdigit() and __line[1] == ".") or (__line[0:2].isdigit() and __line[3] == "."):
            if (self.queryIndentTracker(-1) > self.queryIndentTracker(-2)):
                self.line_type_tracker.append("ol")
            elif (self.queryIndentTracker(-1) < self.queryIndentTracker(-2)):
                self.line_type_tracker.append("/ol")
            elif (self.line_type_tracker[-1] == "ol" or self.line_type_tracker[-1] == "li"):
                self.line_type_tracker.append("li")
            elif (self.line_type_tracker[-1] == "/ol" and len(self.close_out) != 0):
                self.line_type_tracker.append("li")
            else:
                self.line_type_tracker.append("ol")
        elif (__line[0] == ">"):
            if (self.line_type_tracker[-1] == "blockquote" or self.line_type_tracker[-1] == "bqt"):
                self.line_type_tracker.append("bqt")
            else:
                self.line_type_tracker.append("blockquote")
        elif (__line[0:4] == "```"):
            self.line_type_tracker.append("pre")
            self.pre = not self.pre
        else:
            self.line_type_tracker.append("p")

        self.trimTracker(self.line_type_tracker)

    # Method: updateIndentTracker
    # Purpose: Keep track of the indentation level.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line to process, mangled. (String)
    # Return: None
    def updateIndentTracker(self, __line):
        self.line_indent_tracker.append(len(__line) - len(__line.lstrip(' ')))

        self.trimTracker(self.line_indent_tracker)

    # Method: queryIndentTracker
    # Purpose: Return the indent level for the specified line.
    # Parameters:
    # - self: Class namespace
    # - __pos: Desired position, mangled. (Int)
    # Return:
    # - Indent level for specified line. (Int)
    def queryIndentTracker(self, __pos):
        return self.line_indent_tracker[__pos]

    # Method: closeOut
    # Purpose: Write closing HTML tags for any open block-level elements.
    # Parameters:
    # - self: Class namespace
    # Return:
    # - String with each closing HTML tag on its own line. (String)
    def closeOut(self):
        return '\n'.join(self.close_out)

    # Method: escapeCharacters
    # Purpose: Escape &, *, <, and > characters in the text before they are
    # processed as Markdown tags.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line, mangled. (String)
    # Return:
    # - Line with &, *, <, and > escaped using their HTML entities. (String)
    def escapeCharacters(self, __line):
        ## Escape ampersands. Replace them with the appropriate HTML entity.
        __line = __line.replace("&", "&#38;")

        ## Parse escaped asteriscs, to keep them from being interpreted as
        ## asterics indicating bold or italic text.
        __line = __line.replace("\*", "&#42;")

        ## Escape < and > signs
        __line = __line.replace("<", "&lt;").replace(">", "&gt;")

        return __line

    # Method: html
    # Purpose:
    # - 1. Update the trackers with new lines to continue building the HTML
    #      document, and
    # - 2. Ingest raw Markdown line, process it, and return valid HTML.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line, mangled. (String)
    # Return:
    # - Line formatted with HTML. (String)
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

        # Handle code blocks
        if (self.getLineType(-1) == "pre"):
            if (self.pre == True):
                return "<pre>"
            return "</pre>"
        if (self.pre == True):
            return __line

        __line = __line.lstrip(' ')

        __line = self.escapeCharacters(__line)

        if (len(__line) == 0):
            __line = self.closeOut()
            self.close_out = []
            return __line

        # Handle unorered lists
        ## Opening tags
        if (self.getLineType(-1) == "ul"):
            __line = "<ul>"+'\n'+"    <li>"+__line[2:]+"</li>"
            self.close_out.append("</ul>\n")
        ## Closing tags
        elif (self.getLineType(-1) == "/ul"):
            __line = "</ul>\n<li>"+__line[2:]+"</li>"
            self.close_out.remove("</ul>\n")
        # Handle ordered lists
        ## Opening tags
        elif (self.getLineType(-1) == "ol"):
            __line = "<ol>"+'\n'+"    <li>"+". ".join(__line.split(". ")[1:])+"</li>"
            self.close_out.append("</ol>\n")
        ## Closing tags
        elif (self.getLineType(-1) == "/ol"):
            __line = "</ol>\n<li>"+__line[2:]+"</li>"
            self.close_out.remove("</ol>\n")
        # Handle list elements
        elif (self.getLineType(-1) == "li"):
            __line = "    <li>"+__line[2:]+"</li>"
        # Handle blockquotes
        elif (self.getLineType(-1) == "blockquote"):
            __line = "<blockquote>\n    <p>"+__line[5:]+"</p>"
            self.close_out.append("</blockquote>\n")
        elif (self.getLineType(-1) == "bqt"):
            __line = "    <p>"+__line[5:]+"</p>"
        # Handle headers
        elif (self.getLineType(-1) == "header"):
            l = len(__line) - len(__line.lstrip("#"))
            __line = "<h"+str(l)+" id=\""+''.join(ch for ch in __line if ch.isalnum())+"\">"+__line.lstrip("#").rstrip("#").strip()+"</h"+str(l)+">"
            return __line
        # Handle horizontal rules
        elif (self.getLineType(-1) == "hr"):
            return "<hr />"
        # Handle images
        elif (self.getLineType(-1) == "img"):
            __line = __line.split("]")
            desc = __line[0][2:]
            url = __line[1].split(" ")[0][1:]
            alt = __line[1].split(" ")[1][1:-2]
            return "<div class='image'><img src='%s' alt='%s' title='%s' /></div>" % (url, alt, desc)
        # Handle series index
        elif (self.getLineType(-1) == "idx"):
            with open("./Content/System/"+__line[1:-1], "r") as fd:
                __line = "<ul style=\"border:1px dashed gray\" id=\"series_index\">\n"
                for each in fd:
                    __line += "    <li>"+each.strip()+"</li>\n"
                __line += "</ul>"
            return __line
        # Otherwise, treat as a paragraph
        else:
            __line = "<p>"+__line+"</p>"


        __line = self.parseInlineMD(__line)


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