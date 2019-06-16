#!/usr/local/bin/python3

# Import methods
from re import findall # re.findall, for links

class Markdown:
    # Initialize variables
    __line_tracker = ["", "", ""] # Last three lines, raw.
    __line_type_tracker = ["", "", ""] # Type of last three lines.
    __line_indent_tracker = [0, 0, 0] # Indent level of last three lines.
    __close_out = [] # List of block-level elements that still need closed out.
    __pre = False # Yes/no, is the parser in a <pre> tag?

    # Method: __parseInlineMD
    # Purpose: Turn all inline Markdown tags into HTML.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line to process, mangled (String)
    # Return:
    # - Parsed line. (String)
    def __parseInlineMD(self, __line):
        # Parser tracks leading whitespace, so remove it to make parsing the
        # line easier.
        __line = __line.rstrip('\n')
        
        # Parse horizontal rules and emdashes
        __line = __line.replace("---", "<hr />")
        __line = __line.replace("--", "&#160;&#8212;&#160;")

        ## Prase **, or <strong>, tags first, to keep them from being
        ## interpreted as <em> tags...
        while ("**" in __line):
            __line = __line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)

        ## ... then parse the remaining <em> tags. Make sure there is an even
        # number of * to parse as <em> ... </em>.
        if (__line.count("*") % 2 == 0):
            while ("*" in __line):
                # This if skips over the leading "* " in an unordered list, and
                # parses the rest of the line for <em> tags.
                if (__line[0] == "*" and __line[1] == " "):
                    __line = "*"+__line[1:].replace("*", "<em>", 1).replace("*", "</em>", 1)
                    break
                __line = __line.replace("*", "<em>", 1).replace("*", "</em>", 1)

        ## Parse inline code with <code> ... </code> tags.
        while ("`" in __line):
            __line = __line.replace("`", "<code>", 1).replace("`", "</code>", 1)

        ## Parse single quotatin marks.
        __line = __line.replace(" '", " &#8216;").replace("' ", "&#8217; ")

        ## Parse aposrophes.
        __line = __line.replace("'", "&#39;")

        ## Parse double quotation marks.
        __line = __line.replace(' "', " &#8220;").replace('" ', "&#8221; ")

        ## Parse links.
        for each in findall("\[([^\]]+)\]\(([^\)]+)\)", __line):
            __line = __line.replace("["+each[0]+"]("+each[1]+")", "<a href=\""+each[1]+"\">"+each[0]+"</a>")

        return __line

    # Method: __getLineType
    # Purpose: Return the type of line for the specified position.
    # Parameters:
    # - self: Class namespace
    # - __pos: Desired position, mangled.
    # Return:
    # - Type of line at specified position (String)
    def __getLineType(self, __pos):
        return self.__line_type_tracker[__pos]

    # Method: __trimTracker
    # Purpose: Keep tracker lists to a max of three elements.
    # Parameters:
    # - self: Class namespace
    # - __trkr: Reference to tracker to be trimmed.
    # Return: None.
    def __trimTracker(self, __trkr):
        if (len(__trkr) > 3):
            __trkr.pop(0)

    # Method: __updateLineTracker
    # Purpose: Keep track of raw lines.
    # Parameters:
    # - self: Class namespace
    # - __line: Raw Markdown line, mangled.
    # Return: None.
    def __updateLineTracker(self, __line):
        self.__line_tracker.append(__line)
        self.__trimTracker(self.__line_tracker)

    # Method: __updateLineTypeTracker
    # Purpose: Determine type of line, and whether it is part of a larger
    # block-level element, and annotate that in the line type tracker.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line to process, mangled. (String)
    # Return: None.
    def __updateLineTypeTracker(self, __line):
        __line = __line.lstrip(' ')

        if (len(__line) == 0):
            self.__line_type_tracker.append("blank")
        elif (__line[0] == "#"):
            self.__line_type_tracker.append("header")
        elif (__line[0:4] == "---"):
            self.__line_type_tracker.append("hr")
        elif (__line[0:2] == "!["):
            self.__line_type_tracker.append("img")
        elif (__line[0] == "{"):
            self.__line_type_tracker.append("idx")
        elif (__line[0] in ['*', '+', '-'] and __line[1] == ' '):
            if (self.__queryIndentTracker(-1) > self.__queryIndentTracker(-2)):
                self.__line_type_tracker.append("ul")
            elif (self.__queryIndentTracker(-1) < self.__queryIndentTracker(-2)):
                self.__line_type_tracker.append("/ul")
            elif (self.__line_type_tracker[-1] == "ul" or self.__line_type_tracker[-1] == "li"):
                self.__line_type_tracker.append("li")
            elif (len(self.__close_out) != 0):
                self.__line_type_tracker.append("li")
            else:
                self.__line_type_tracker.append("ul")
        elif (__line[0].isdigit() and __line[1] == ".") or (__line[0:2].isdigit() and __line[3] == "."):
            if (self.__queryIndentTracker(-1) > self.__queryIndentTracker(-2)):
                self.__line_type_tracker.append("ol")
            elif (self.__queryIndentTracker(-1) < self.__queryIndentTracker(-2)):
                self.__line_type_tracker.append("/ol")
            elif (self.__line_type_tracker[-1] == "ol" or self.__line_type_tracker[-1] == "li"):
                self.__line_type_tracker.append("li")
            elif (self.__line_type_tracker[-1] == "/ol" and len(self.__close_out) != 0):
                self.__line_type_tracker.append("li")
            else:
                self.__line_type_tracker.append("ol")
        elif (__line[0] == ">"):
            if (self.__line_type_tracker[-1] == "blockquote" or self.__line_type_tracker[-1] == "bqt"):
                self.__line_type_tracker.append("bqt")
            else:
                self.__line_type_tracker.append("blockquote")
        elif (__line[0:4] == "```"):
            self.__line_type_tracker.append("pre")
            self.__pre = not self.__pre
        else:
            self.__line_type_tracker.append("p")

        self.__trimTracker(self.__line_type_tracker)

    # Method: __updateIndentTracker
    # Purpose: Keep track of the indentation level.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line to process, mangled. (String)
    # Return: None
    def __updateIndentTracker(self, __line):
        self.__line_indent_tracker.append(len(__line) - len(__line.lstrip(' ')))

        self.__trimTracker(self.__line_indent_tracker)

    # Method: __queryIndentTracker
    # Purpose: Return the indent level for the specified line.
    # Parameters:
    # - self: Class namespace
    # - __pos: Desired position, mangled. (Int)
    # Return:
    # - Indent level for specified line. (Int)
    def __queryIndentTracker(self, __pos):
        return self.__line_indent_tracker[__pos]

    # Method: __closeOut
    # Purpose: Write closing HTML tags for any open block-level elements.
    # Parameters:
    # - self: Class namespace
    # Return:
    # - String with each closing HTML tag on its own line. (String)
    def __closeOut(self):
        return '\n'.join(self.__close_out)

    # Method: __escapeCharacters
    # Purpose: Escape &, *, <, and > characters in the text before they are
    # processed as Markdown tags.
    # Parameters:
    # - self: Class namespace
    # - __line: Input line, mangled. (String)
    # Return:
    # - Line with &, *, <, and > escaped using their HTML entities. (String)
    def __escapeCharacters(self, __line):
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

        self.__updateIndentTracker(__line)
        self.__updateLineTracker(__line)
        self.__updateLineTypeTracker(__line)

        print(self.__line_tracker)
        print(self.__line_type_tracker)
        print(self.__line_indent_tracker)
        print()

        # Handle code blocks
        if (self.__getLineType(-1) == "pre"):
            if (self.__pre == True):
                return "<pre>"
            return "</pre>"
        if (self.__pre == True):
            return __line

        __line = __line.lstrip(' ')

        __line = self.__escapeCharacters(__line)

        if (len(__line) == 0):
            __line = self.__closeOut()
            self.__close_out = []
            return __line

        # Handle unorered lists
        ## Opening tags
        if (self.__getLineType(-1) == "ul"):
            __line = "<ul>"+'\n'+"    <li>"+__line[2:]+"</li>"
            self.__close_out.append("</ul>\n")
        ## Closing tags
        elif (self.__getLineType(-1) == "/ul"):
            __line = "</ul>\n<li>"+__line[2:]+"</li>"
            self.__close_out.remove("</ul>\n")
        # Handle ordered lists
        ## Opening tags
        elif (self.__getLineType(-1) == "ol"):
            __line = "<ol>"+'\n'+"    <li>"+". ".join(__line.split(". ")[1:])+"</li>"
            self.__close_out.append("</ol>\n")
        ## Closing tags
        elif (self.__getLineType(-1) == "/ol"):
            __line = "</ol>\n<li>"+__line[2:]+"</li>"
            self.__close_out.remove("</ol>\n")
        # Handle list elements
        elif (self.__getLineType(-1) == "li"):
            __line = "    <li>"+__line[2:]+"</li>"
        # Handle blockquotes
        elif (self.__getLineType(-1) == "blockquote"):
            __line = "<blockquote>\n    <p>"+__line[5:]+"</p>"
            self.__close_out.append("</blockquote>\n")
        elif (self.__getLineType(-1) == "bqt"):
            __line = "    <p>"+__line[5:]+"</p>"
        # Handle headers
        elif (self.__getLineType(-1) == "header"):
            l = len(__line) - len(__line.lstrip("#"))
            __line = "<h"+str(l)+" id=\""+''.join(ch for ch in __line if ch.isalnum())+"\">"+__line.lstrip("#").rstrip("#").strip()+"</h"+str(l)+">"
            return __line
        # Handle horizontal rules
        elif (self.__getLineType(-1) == "hr"):
            return "<hr />"
        # Handle images
        elif (self.__getLineType(-1) == "img"):
            __line = __line.split("]")
            desc = __line[0][2:]
            url = __line[1].split(" ")[0][1:]
            alt = __line[1].split(" ")[1][1:-2]
            return "<div class='image'><img src='%s' alt='%s' title='%s' /></div>" % (url, alt, desc)
        # Handle series index
        elif (self.__getLineType(-1) == "idx"):
            with open("./Content/System/"+__line[1:-1], "r") as fd:
                __line = "<ul style=\"border:1px dashed gray\" id=\"series_index\">\n"
                for each in fd:
                    __line += "    <li>"+each.strip()+"</li>\n"
                __line += "</ul>"
            return __line
        # Otherwise, treat as a paragraph
        else:
            __line = "<p>"+__line+"</p>"


        __line = self.__parseInlineMD(__line)

        return __line