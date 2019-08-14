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
    # m = get_m()
    m = Markdown()
    open("/Users/zjszewczyk/Desktop/ThreadTest/"+tgt.replace(".txt", ".html"), "w").close()
    with open("./Content/"+tgt, "r") as fd, open("/Users/zjszewczyk/Desktop/ThreadTest/"+tgt.replace(".txt", ".html"), "a") as o_fd:
        for line in fd:
            o_fd.write(m.html(line)+'\n')
    del m

t1 = datetime.datetime.now()
files = []
for each in listdir("./Content"):
    if (".txt" in each):
        handle_file(each)
t2 = datetime.datetime.now()
print(("Normal execution time: "+str(t2-t1)+"s"))

files = []
for each in listdir("./Content"):
    if (".txt" in each):
        files.append(each)

t1 = datetime.datetime.now()
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(handle_file, files)
t2 = datetime.datetime.now()
print(("Threading execution time: "+str(t2-t1)+"s"))

t1 = datetime.datetime.now()
import multiprocessing
with multiprocessing.Pool() as pool:
    pool.map(handle_file, files)
t2 = datetime.datetime.now()
print(("Multiprocessing execution time: "+str(t2-t1)+"s"))