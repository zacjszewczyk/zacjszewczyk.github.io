#!/usr/local/bin/python3

from Markdown2 import Markdown
from time import sleep

# m = Markdown("https://zacs.site/")
m = Markdown()

open("out.html", "w").close()

with open("./Content/Complete Overhaul.txt", "r") as fd, open("out.html", "a") as o_fd:
    for line in fd:
        sleep(0.1)
        o_fd.write(m.html(line)+'\n')