#!/usr/local/bin/python3

from Markdown2 import Markdown
import datetime
from os import listdir
import threading
import concurrent.futures

thread_local = threading.local()

def get_m():
    if not hasattr(thread_local, "m"):
        thread_local.m = Markdown()
    return thread_local.m

def handle_file(tgt):
    m = get_m()
    open("/Users/zjszewczyk/Desktop/ThreadTest/"+tgt.replace(".txt", ".html"), "w").close()
    with open("./Content/"+tgt, "r") as fd, open("/Users/zjszewczyk/Desktop/ThreadTest/"+tgt.replace(".txt", ".html"), "a") as o_fd:
        for line in fd:
            o_fd.write(m.html(line)+'\n')

t1 = datetime.datetime.now()

for each in listdir("./Content"):
    if (".txt" in each):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(handle_file, each)
        # handle_file(each)

t2 = datetime.datetime.now()
print(("Execution time: "+str(t2-t1)+"s"))