#!C:/Python32/python.exe

import os

for each in os.listdir():
    print (each)
    if each.endswith(".txt") == False and each.endswith(".py") == False:
        for every in os.listdir(each):
            print ("    "+every)
            os.system("mv \""+each+"/"+every+"\" \""+every+"\"")