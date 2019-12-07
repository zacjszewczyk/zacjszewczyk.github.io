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
        # # Year
        # print(o[0])
        # for month in o[1]:
        #     # Month
        #     print("  "+o[0]+"-"+month)
        #     for day in o[1][month]:
        #         # Day
        #         print("    "+o[0]+"-"+month+"-"+day)
        #         for timestamp in o[1][month][day]:
        #             # Individual articles by time
        #             print("      "+o[0]+"-"+month+"-"+day+"-"+timestamp+"_"+o[1][month][day][timestamp])


        # For each year in which a post was made, generate a 'year' file, that
        # contains links to each month in which a post was published.

        # Clear the 'year' file
        open("./local/blog/"+o[0]+".html", "w", encoding=ENCODING).close()
        year_fd = open("./local/blog/"+o[0]+".html", "a", encoding=ENCODING)
        # Write the opening HTML tags
        year_fd.write(content[2].replace("{{ title }}", "Post Archives - ").replace("{{ BODYID }}", "archives", 1))
        # Display the months listed.
        year_fd.write("<div id=\"years_index\">\n<div>%s</div>\n" % (o[0]))
        # Sort the sub-dictionaries by keys, months, then iterate over it. For each
        # month in which a post was made, generate a 'month' file that contains all
        # posts made during that month.
        for month in sorted(files[o[0]], reverse=True):
            # Add a link to the month, to the year file it belongs to.
            year_fd.write("<div><a href=\"%s\">%s</a></div>" % (o[0]+"-"+month+".html", months[month]))
            # Clear the 'month' file
            open("./local/blog/"+o[0]+"-"+month+".html", "w", encoding=ENCODING).close()
            month_fd = open("./local/blog/"+o[0]+"-"+month+".html", "a", encoding=ENCODING)
            # Write the opening HTML tags
            month_fd.write(content[2].replace("{{ title }}", "Post Archives - ").replace("{{ BODYID }}", "archives", 1).replace("<!--BLOCK HEADER-->", "<article>\n<p>\n"+months[month]+", <a href=\""+o[0]+".html\">"+o[0]+"</a>\n</p>\n</article>", 1))

            # Sort the sub-dictionaries by keys, days, then iterate over it.
            for day in sorted(files[o[0]][month], reverse=True):
                # Sort the sub-dictionaries by keys, timestamps, then iterate over it
                for timestamp in sorted(files[o[0]][month][day], reverse=True):
                    # If a structure file already exists, don't rebuild the HTML file for individual articles
                    if (not isfile("./local/blog/"+files[o[0]][month][day][timestamp].lower().replace(" ","-")[0:-3]+"html")):
                        GenPage(files[o[0]][month][day][timestamp], "%s/%s/%s %s" % (o[0], month, day, timestamp))
                    else:
                        if (CompareMtimes("./Content/"+files[o[0]][month][day][timestamp], "./local/blog/"+files[o[0]][month][day][timestamp].lower().replace(" ","-")[0:-3]+"html")):
                            pass
                        else:
                            # Generate each content file. "year", "month", "day", "timestamp"
                            # identify the file in the dictionary, and the passed time values
                            # designate the desired update time to set the content file.
                            GenPage(files[o[0]][month][day][timestamp], "%s/%s/%s %s" % (o[0], month, day, timestamp))

                    # For each article made in the month, add an entry on the appropriate
                    # 'month' structure file.
                    month_fd.write("<article>\n    %s<a href=\"%s\">%s</a>\n</article>\n" % (o[0]+"/"+month+"/"+day+" "+timestamp+": ", files[o[0]][month][day][timestamp].lower().replace(" ", "-")[0:-3]+"html", trip()))

            # Write closing HTML tags to the month file.
            month_fd.write(content[1].replace("assets/", "../assets/"))
            month_fd.close()

        # Write closing HTML tags to the year file.
        year_fd.write("</div>\n"+content[1].replace("assets/", "../assets/"))
        year_fd.close()

        # Cleanup
        del year_fd, month_fd



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