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

### Import modules
from sys import exit, argv, stdout, stdin # Command line interface
from tty import setraw, setcbreak # Raw input
from termios import tcgetattr, tcsetattr, TCSAFLUSH # Backup/resume shell
from os.path import exists # Reading input files
from os import popen # Detect terminal size
from re import sub # Change menu to try to avoid text wrapping

# Method: GetUserSelection
# Purpose: Display a menu for the user, allowing for cursor movement.
# Parameters:
# - prompt: Items to prompt the user with (List)
def GetUserSelection(options):
        # Bounds check
        if (len(options) < 2):
                print(c.FAIL+"Error: Not enough options."+c.ENDC)

        # Backup the shell session, to restore it later. Set the stage.
        backup = tcgetattr(stdin)
        setraw(stdin)
        index = 0

        # Continue accepting input until the user aborts the process (CTRL-C)
        # or hits the enter key.
        while True:
                # Print menu
                for i, each in enumerate(options):
                        if (i == index):
                                stdout.write(u"\u25C9 %s\u001b[1000D\n" % (each))
                        else:
                                stdout.write(u"\u25EF %s\u001b[1000D\n" % (each))
                stdout.write(u"\u001b[1000D")

                # Read a single character and get its code.
                char = ord(stdin.read(1))

                # Manage internal data-model
                if char == 3: # CTRL-C
                        # Restore shell session from backup, then exit.
                        tcsetattr(stdin, TCSAFLUSH, backup)
                        return
                elif char in {10, 13}: # Enter key
                        # Restore shell session from backup, then exit the loop.
                        tcsetattr(stdin, TCSAFLUSH, backup)
                        break
                elif char == 27: # Arrow keys
                        # Accept input from arrow keys and move the cursor accordingly
                        next1, next2 = ord(stdin.read(1)), ord(stdin.read(1))
                        if next1 == 91:
                                if next2 == 65: # Up
                                        index = max(index-1,0)
                                elif next2 == 66: # Down
                                        index = min(index+1,len(options)-1)
                # Clear menu
                for i in range(1,len(options)+1):
                        stdout.write(u"\u001b[1A")
                        stdout.write(u"\u001b[0J")
        return options[index]

categories = ['Tech', 'Politics', 'Uncategorized', 'Finances', 'Writing', 'Programming', 'Podcasts', 'Simple living', 'Readme', 'Gear', 'Travel', 'Motivation', 'Overlanding', 'Weightlifting', 'Blogging', 'Politcs', 'Preparedness', "Cybersecurity", "Personal Development", "Professional Development"]

for each in listdir("./content"):
    each = f"./content/{each}"
    if (each[-4:] != ".txt"): continue

    fd = open(each,"r")
    if ("Category" in {y[0].strip():y[1].strip() for y in [x.split(": ") for x in fd.readlines()[0:6] if x != '\n']}.keys()):
        continue

    print(f"\nChoosting for {each}")
    f = open(each, "r")
    contents = f.readlines()
    f.close()
    print("\n".join(contents))

    cat = GetUserSelection(categories)
    if (cat == None):
        break

    print(f"Chose '{cat}' for '{each}'")

    contents.insert(4, f"Category: {cat}\n")

    f = open(each, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

    fd = open(each, "r")
    mtime = mktime(strptime(fd.readlines()[3][9:].strip(), "%Y/%m/%d %H:%M:%S"))
    fd.close()
    utime(each, (mtime, mtime))