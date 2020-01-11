#!/usr/local/bin/python3

from os import listdir # Enumerating directories
from ModTimes import CompareMtimes # Compare file mod times
from os.path import isfile # File existence operations

def CompareContent(fname):
    published_fd = open("./Content/"+fname, "r")
    local_fd = open("/Users/zjszewczyk/Dropbox/Writing/Blog/"+fname, "r")

    for i,line in enumerate(published_fd):
        if line.strip() != local_fd.readline().strip():
            return False

    published_fd.close()
    local_fd.close()

    return True

# List of published posts
published_posts = []
# List of local posts
local_posts = []
# Lists of same posts
same_posts = []
# Lists of posts that do not exist in deploy directory
do_not_exist = []
# List of posts with different mtimes
different_mtimes = []
# List of posts with different content
different_content = []

for i,each in enumerate(listdir("./Content/")):
    if (each.endswith(".txt")):
        # print(i,each)
        published_posts.append(each)
    else:
        pass
        # print(i,each)

for i,each in enumerate(listdir("/Users/zjszewczyk/Dropbox/Writing/Blog/")):
    if (each.endswith(".txt")):
        # print(i,each)
        local_posts.append(each)
    else:
        pass
        # print(i,each)

print("Published posts:",len(published_posts))
print("Local posts:",len(local_posts))

for i,each in enumerate(local_posts):
    if (isfile("./Content/"+each)):
        pass
    else:
        do_not_exist.append(each)
        continue

    if (CompareMtimes("./Content/"+each, "/Users/zjszewczyk/Dropbox/Writing/Blog/"+each)):
        pass
    else:
        different_mtimes.append(each)
        continue

    if (CompareContent(each)):
        pass
    else:
        different_content.append(each)
        continue

    # print ("./Content/"+each,"and","/Users/zjszewczyk/Dropbox/Writing/Blog/"+each,"are the same.")
    same_posts.append(each)

print("Local, unpublished posts:",len(do_not_exist))
print("Posts with different mtimes:",len(different_mtimes))
print("Posts with different content:",len(different_content))
print("Same posts:",len(same_posts))
print()
print("Local, unpublished posts:")
for i,each in enumerate(do_not_exist):
    print("    ",i,":",each)