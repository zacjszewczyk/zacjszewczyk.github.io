#!/usr/local/Cellar/python/3.7.3/bin/python3

import re

class Markdown:

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

    def html(self, line):
        