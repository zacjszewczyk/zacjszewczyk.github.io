#!/usr/local/bin/python3

import os

for each in os.listdir("./Content"):
    if (each.endswith(".txt")):        
        print(each)

        with open("./Content/"+each, "r") as src_fd, open("./Content2/"+each, "w") as dst_fd:
            content = ""
            for line in iter(src_fd):
                if (line.startswith("    ")):
                    content += "> "+line.strip()+'\n'
                else:
                    content += line.strip()+'\n'

            dst_fd.write(content)

        print("##################\n\n")