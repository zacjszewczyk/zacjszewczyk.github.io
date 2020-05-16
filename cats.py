#!/usr/bin/python3

from os import listdir, system, utime, remove, rename
from time import mktime, strptime

def migrate():
    content_files = set(listdir("./content"))
    category_files = set(listdir("/Users/zjszewczyk/Desktop/Categories"))

    # cp -n ./content/* ~/Desktop/Categories
    # print(content_files.difference(category_files))

    categories = []

    for each in category_files:
        if (each[-4:] != ".txt"): continue

        category_fd = open(f"/Users/zjszewczyk/Desktop/Categories/{each}", "r")
        cat_line = category_fd.readlines()[5].strip()

        if ("Category" in cat_line):
            category_fd.seek(0)
            # print(each)
            # print(cat_line)

            category = cat_line.split(": ")[1]

            source_fd = open(f"./content/{each}", "r")

            open(f"./content/{each}.tmp", "w").close()
            d_fd = open(f"./content/{each}.tmp", "a")

            for i,line in enumerate(source_fd):
                if (i == 3):
                    mtime = mktime(strptime(line[9:].strip(), "%Y/%m/%d %H:%M:%S"))
                if (i == 4):
                    d_fd.write(cat_line+"\n")

                d_fd.write(line)

            else:
                d_fd.close()
                # system(f"uniq './content/{each}.tmp' | tee './content/{each}.tmp'")
                utime(f"./content/{each}.tmp", (mtime, mtime))

            if (category not in categories): categories.append(category)

            source_fd.close()

            remove(f"./content/{each}")
            rename(f"./content/{each}.tmp", f"./content/{each}")

        category_fd.close()

    print("Categories:",categories)

categories = ['Tech', 'Politics', 'Uncategorized', 'Finances', 'Writing', 'Programming', 'Podcasts', 'Simple living', 'Readme', 'Gear', 'Travel', 'Motivation', 'Overlanding', 'Weightlifting', 'Blogging', 'Politcs', 'Preparedness']
