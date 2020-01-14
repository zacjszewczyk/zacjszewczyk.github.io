#!/usr/local/bin/python3

import timeit as t

#print "os.path.getmtime:\t",t.timeit("os.path.getmtime('test.sh')","import os",number=10000)
#print "os.stat:\t\t",t.timeit("os.stat('test.sh').st_mtime","import os", number=10000)

import os
import time

#print "vars:\t\t",t.timeit("print '%d/%d/%d/%d:%d:%d' % (t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)","import time; import os; t = time.localtime(os.stat('test.sh').st_mtime)",number=10000)
#print "vars:\t\t",t.timeit("print time.strftime('%Y/%m/%d/%H:%M:%S', t)","import time; import os; t = time.localtime(os.stat('test.sh').st_mtime)",number=10000)

#print "replace:\t\t",t.timeit("string.replace('things','nothing')","string = 'Temp string with some things in it.'",number=10000)
#print "re.sub:\t\t",t.timeit("re.sub('things','nothing',string)","import re; string = 'Temp string with some things in it.'",number=10000)

# print "endswith:\t",t.timeit("each.endswith('.txt')","each = 'Were Live.txt'", number=10000)
# print "in:\t\t",t.timeit("'.txt' in each","each = 'Were Live.txt'", number=10000)
# print "index:\t\t",t.timeit("'txt' == each[-3:]","each = 'Were Live.txt'", number=10000)

# print "endswith:\t",t.timeit("each.startswith('http')","each = 'http://Were Live.txt'", number=10000)
# print "index:\t\t",t.timeit("'http' == each[0:4]","each = 'http://Were Live.txt'", number=10000)

# print "string.lower():\t",t.timeit("each.lower()","each='Conjecture Regarding Larger iPhone Displays.txt'", number=10000)
# func = """\
# import string
# letter_set = frozenset(string.ascii_lowercase + string.ascii_uppercase)
# tab = string.maketrans(string.ascii_lowercase + string.ascii_uppercase,string.ascii_lowercase * 2)
# deletions = ''.join(ch for ch in map(chr,range(256)) if ch not in letter_set)
# each='Conjecture Regarding Larger iPhone Displays.txt'
# def makelower(s):
#     return string.translate(s, tab, deletions)"""
# to_exec = "makelower(each)"
# print "translate:\t",t.timeit(stmt=to_exec,setup=func, number=10000)

# environment = """\
# from sys import modules
# from sys import stdout
# """
# to_exec = "from sys import stdout"
# print "duplicate:\t",t.timeit(stmt=to_exec,setup=environment, number=10000)
# environment = """\
# from sys import modules
# """
# to_exec = """\
# if ("stdout" not in modules.keys()):
#     from sys import modules
# """
# print "check:\t\t",t.timeit(stmt=to_exec,setup=environment, number=10000)

# environment = """\
# line = \"Hello my name is Zac.\""""
# to_exec = "line[0].isalpha()"
# print("isalpha:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# environment = """\
# from re import match
# line = \"Hello my name is Zac.\""""
# to_exec = """\
# match('[a-zA-Z]', line[0])
# """
# print("regex:\t\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

# environment = """\
# line = "Consumers tend to allow the wrong factors to influence this process. Blind loyalty, because their family has always driven a certain brand. Nationalism, as if the parent company's owners' nationality ought to influence one of the most expensive investments they will ever make. Fuel efficiency when gas prices peak, yet casual disregard for it when they fall. Marketing campaigns. Fad technologies. People buy cars for all sorts of bad reasons, but I wanted to do better. How could I strip away folk wisdom, ignorance, and short-sightedness, though? How could I ignore all the tired tropes, and the flashy accessories, to find vehicles whose cost best matched their worth? I could do this by focusing not on the sticker price, a figure the manufacturer believes most consumers will value their product at because of the factors above, but rather by focusing on reliability and longevity--two metrics I could approximate as one, by examining resale value. Years down the road, when they have traded those ephemeral criteria for meaningful ones, the amount of money the average person will exchange for a given vehicle is a much better measure of its actual worth. This is the criterion by which I began narrowing my search."
# """
# to_exec = """\
# if ("--" in line):
#     line = line.replace("--", "&#160;&#8212;&#160;")
# """
# print("check first:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# # environment = """\
# # """
# to_exec = """\
# line = line.replace("&", "&#38;")
# """
# print("no check:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

# environment = """\
# line = "## Title here"
# """
# to_exec = """\
# i = 0
# for ch in line:
#     if (ch == " "):
#         break
#     elif (ch == "#"):
#         i += 1
# print(i)
# """
# print("loop:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# # environment = """\
# # """
# to_exec = """\
# len(line) - len(line.lstrip("#"))
# """
# print("no check:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

# environment = """\
# import re
# em = re.compile(r"\*[^\*]+\*")
# line = 'I dont have an infant son to take care of, so I cannot speak to that adventure, but I can speak to its effects: every so often I undergo bouts of insomnia-like symptoms where no matter how much I may want to sleep, regardless of how significantly tomorrows test will effect my grade, its all I can do to hold myself still while my mind races. *What am I doing tomorrow? Did I finish all my homework? Will I have time to listen to that latest podcast episode? How about write? Its been far too long since Ive written anything but a link post. But I have so many articles in Instapaper...will I have time to finish them tomorrow?* They say those who sleep well at night will never possess the perspective to truly appreciate the inability to sleep, and I completely agree with that: shortly after these experiences end, as I forget how truly terrible the last few nights were, even I begin to lose perspective; it really wasnt *that* bad, after all. But losing sleep is: I never feel motivated to do anything, nothing interests me, I have a short temper and an even shorter tolerance for others, everything loses its luster, and the list goes on and on. Least of all, I feel the urge to create: thats the last thing I want to do after managing to fall asleep only to wake up a few hours later. I can only imagine how rough Sid has it right now.'
# """
# to_exec = r"""
# ## Parse double quotation marks.
# if (line.count("*") % 2 == 0):
#     while ("*" in line):
#         # This if skips over the leading "* " in an unordered list, and
#         # parses the rest of the line for <em> tags.
#         if (line[0] == "*" and line[1] == " "):
#             line = "*"+line[1:].replace("*", "<em>", 1).replace("*", "</em>", 1)
#             break
#         line = line.replace("*", "<em>", 1).replace("*", "</em>", 1)
# """
# print("while:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# to_exec = r"""
# # Parse double-quote quotations
# for each in re.findall("\*[^\*]+\*", line):
#     line = line.replace(each, each.replace('*', "<em>", 1).replace('*', "</em>", 1))
# """
# print("regex:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

# environment = """\
# import re
# line = 'I dont have an infant son to take care of, so I cannot speak to that adventure, but I can speak to its effects: every so often I undergo bouts of insomnia-like symptoms where no matter how AT&T \*much I may want to sleep, regardless &copy; of how significantly & tomorrows test will effect my grade, its all I can do to hold\* myself still while my mind races.'
# """
# to_exec = """
# line = line.replace("<", "&#42;").replace(">", "&#43;")
# """
# print(".replace:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# to_exec = r"""
# # Parse double-quote quotations
# re.sub(r"<", r"&#42;", line)
# re.sub(r">", r"&#43;", line)
# """
# print("regex:\t\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

# environment = """\
# import os
# """
# to_exec = """
# for each in os.listdir("./Content"):
#     pass
# """
# print("listdir:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# to_exec = """
# for dirpath, dirnames, filenames in os.walk('./Content'):
#     for f in filenames:
#         pass
#     break
# """
# print("os.walk:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

# environment = """"""
# to_exec = """
# with open("./blog.py", "r") as fd:
#     fd.readline()
# """
# print("with:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# to_exec = """
# fd = open("./blog.py", "r")
# fd.readline()
# fd.close()

# """
# print("open:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

# environment = """
# import re
# def sylco(word) :

#     word = word.lower()

#     # exception_add are words that need extra syllables
#     # exception_del are words that need less syllables
    
#     exception_add = ['serious','crucial']
#     exception_del = ['fortunately','unfortunately']
    
#     co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
#     co_two = ['coapt','coed','coinci']
    
#     pre_one = ['preach']
    

#     syls = 0 #added syllable number
#     disc = 0 #discarded syllable number

#     #1) if letters < 3 : return 1
#     if len(word) <= 3 :
#         syls = 1
#         return syls
    
#     #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
#     # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

#     if word[-2:] == "es" or word[-2:] == "ed" :
#         doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
#         if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
#             if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
#                 pass
#             else :
#                 disc+=1
    
#     #3) discard trailing "e", except where ending is "le"  
   
#     le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
    
#     if word[-1:] == "e" :
#         if word[-2:] == "le" and word not in le_except :
#             pass
        
#         else :
#             disc+=1
    
#     #4) check if consecutive vowels exists, triplets or pairs, count them as one.

#     doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
#     tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
#     disc+=doubleAndtripple + tripple
    
#     #5) count remaining vowels in word.
#     numVowels = len(re.findall(r'[eaoui]',word))

#     #6) add one if starts with "mc"
#     if word[:2] == "mc" :
#         syls+=1
        
#     #7) add one if ends with "y" but is not surrouned by vowel
#     if word[-1:] == "y" and word[-2] not in "aeoui" :
#         syls +=1
        
#     #8) add one if "y" is surrounded by non-vowels and is not in the last word.
    
#     for i,j in enumerate(word) :
#         if j == "y" :
#             if (i != 0) and (i != len(word)-1) :
#                 if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
#                     syls+=1
    
    
#     #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.
    
#     if word[:3] == "tri" and word[3] in "aeoui" :
#         syls+=1
    
#     if word[:2] == "bi" and word[2] in "aeoui" :
#         syls+=1
    
#     #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"
    
#     if word[-3:] == "ian" : 
#     #and (word[-4:] != "cian" or word[-4:] != "tian") :
#         if word[-4:] == "cian" or word[-4:] == "tian" :
#             pass
#         else :
#             syls+=1
    
#     #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
    
#     if word[:2] == "co" and word[2] in 'eaoui' :
    
#         if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
#             syls+=1
#         elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
#             pass
#         else :
#             syls+=1

#     #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

#     if word[:3] == "pre" and word[3] in 'eaoui' :
#         if word[:6] in pre_one :
#             pass
#         else :
#             syls+=1

#     #13) check for "-n't" and cross match with dictionary to add syllable.
    
#     negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]
    
#     if word[-3:] == "n't" :
#         if word in negative :
#             syls+=1
#         else :
#             pass   

#     #14) Handling the exceptional words.
   
#     if word in exception_del :
#         disc+=1
        
#     if word in exception_add :
#         syls+=1     
    
        
#     # calculate the output
#     return numVowels - disc + syls
# string = "A very cool video on a very cool subject: importing one of the awesome adventure rigs available in other parts of the world, to the United States. Bryan Rogala does a nice job breaking this process down, and shows off Brett Wilhelm's neat Toyota Townace, too."
# """
# to_exec = """
# for word in string.split(" "):
#     sylls = sylco(word)
# """
# print("old:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
# environment = """\
# from re import findall
# def MySyllableCount(word):
#     word = word.lower()

#     syls = 0 # Number of added syllables
#     disc = 0 # Number of discarded syllables

#     #1) If three or less letters, one syllable
#     if len(word) <= 3 :
#         return 1

#     #2) If doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
#     # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)
#     double_vowel = len(findall(r'[eaoui][eaoui]',word))

#     if word[-2:] in ["es", "ed"]:
#         if double_vowel > 1 or len(findall(r'[eaoui][^eaoui]',word)) > 1 :
#             if word[-3:] in ["ted", "tes", "ses", "ied", "ies"]:
#                 pass
#             else:
#                 disc+=1

#     #3) discard trailing "e", except where ending is "le"  
#     if word[-1:] == "e" :
#         if word[-2:] == "le" and word not in ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']:
#             pass
#         else :
#             disc+=1

#     #4) check if consecutive vowels exists, triplets or pairs, count them as one.
#     disc += double_vowel + len(findall(r'[eaoui][eaoui][eaoui]',word))

#     #5) count remaining vowels in word.
#     numVowels = len(findall(r'[eaoui]',word))

#     #6) add one if starts with "mc"
#     if word[:2] == "mc" :
#         syls+=1

#     #7) add one if ends with "y" but is not surrouned by vowel
#     if word[-1:] == "y" and word[-2] not in "aeoui" :
#         syls +=1

#     #8) add one if "y" is surrounded by non-vowels and is not in the last word.
#     for i,j in enumerate(word) :
#         if j == "y" :
#             if (i != 0) and (i != len(word)-1) :
#                 if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
#                     syls+=1

#     #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.
#     if word[:3] == "tri" and word[3] in "aeoui" :
#         syls+=1

#     if word[:2] == "bi" and word[2] in "aeoui" :
#         syls+=1

#     #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"
#     if word[-3:] == "ian" : 
#         if word[-4:] in ["cian", "tian"]:
#             pass
#         else :
#             syls+=1

#     #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
#     if word[:2] == "co" and word[2] in 'eaoui' :
#         if (set(['coapt','coed','coinci']).intersection([word[:4], word[:5], word[:6]])):
#             syls+=1
#         elif (set(['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']).intersection([word[:4], word[:5], word[:6]])):
#             pass
#         else :
#             syls+=1

#     #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
#     if word[:3] == "pre" and word[3] in 'eaoui' :
#         if word[:6] in ['preach']:
#             pass
#         else :
#             syls+=1

#     #13) check for "-n't" and cross match with dictionary to add syllable.
#     if word[-3:] == "n't" :
#         if word in ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]:
#             syls+=1
#         else:
#             pass

#     #14) Handling the exceptional words.
#     # exception_del are words that need less syllables
#     if word in ['fortunately','unfortunately']:
#         disc+=1
#     # exception_add are words that need extra syllables
#     if word in ['serious','crucial']:
#         syls+=1     

#     # calculate the output
#     return numVowels - disc + syls
# string = "A very cool video on a very cool subject: importing one of the awesome adventure rigs available in other parts of the world, to the United States. Bryan Rogala does a nice job breaking this process down, and shows off Brett Wilhelm's neat Toyota Townace, too."
# """
# to_exec = """
# for word in string.split(" "):
#     sylls = MySyllableCount(word)
# """
# print("new:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))

environment = """\
name = "Zac"
location = "Georgia"
"""
to_exec = """
print(f"Hi, I'm {name} from {location}")
"""
print("Time: f-strings:\t",t.timeit(stmt=to_exec,setup=environment, number=10000))
to_exec = """\
print("Hi, I'm %s from %s" % (name, location))
"""
print("Time: %%s:\t\t",t.timeit(stmt=to_exec,setup=environment, number=10000))