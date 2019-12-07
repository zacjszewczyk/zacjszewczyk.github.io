#!/usr/local/bin/python3

# multiprocessing
from multiprocessing import Pool

# files dictionary
from os import listdir, stat
from time import strftime, localtime
from datetime import datetime

# file operations
from locale import getpreferredencoding

# Global variables
ENCODING = getpreferredencoding()

class Orchestrator:
    from Markdown2 import Markdown

    def __init__(self, o):
        self.md = self.Markdown("https://zacs.site")

        print(o[0])
        for month in o[1]:
            print("  "+o[0]+"-"+month)
            for day in o[1][month]:
                print("    "+o[0]+"-"+month+"-"+day)



    def __del__(self):
        del self.md

t1 = datetime.now()

files = {}

for each in listdir("Content"):
    if (".txt" in each):
        mtime = strftime("%Y/%m/%d/%H:%M:%S", localtime(stat("Content/"+each).st_mtime)).split("/")
        if (mtime[0] not in files):
            files[mtime[0]] = {}
        if (mtime[1] not in files[mtime[0]]):
            files[mtime[0]][mtime[1]] = {}
        if (mtime[2] not in files[mtime[0]][mtime[1]]):
            files[mtime[0]][mtime[1]][mtime[2]] = {}
        if (mtime[3] not in files[mtime[0]][mtime[1]][mtime[2]]):
            files[mtime[0]][mtime[1]][mtime[2]][mtime[3]] = {}
        files[mtime[0]][mtime[1]][mtime[2]][mtime[3]] = each

# for year in files:
#     print(year)
#     for month in files[year]:
#         print("  "+month)
#         for day in files[year][month]:
#             print("    "+day)
#             for time in files[year][month][day]:
#                 print("      "+time)
#                 print("        "+files[year][month][day][time])

pool = Pool()
pool.map(Orchestrator, files.items())

t2 = datetime.now()
print("Execution time: "+str(t2-t1)+"s")