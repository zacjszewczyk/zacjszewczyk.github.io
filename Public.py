#!/usr/local/bin/python3

# Imports
from sys import argv # Verbose
from os import remove, mkdir # Clearing deployment folder
from os.path import isdir # Dirs
from shutil import rmtree, copy, copytree # Deployment
from CLI import c # Output styling
from os import listdir # Enumeration
from os import utime # Output file time mod
from time import time # Time

# Target directory for public deployment
dst = "/Users/zjszewczyk/Dropbox/Code/Public/FirstCrack/"

# Method: CopyToDeploy
# Purpose: Copy the required files and folders to the deployment directory.
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def CopyToDeploy(v=False):
    # Copy "README.md" to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"README.md'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./README.md", dst+"README.md")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy "makefile" to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"makefile'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./makefile", dst+"makefile")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the blog.py to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"blog.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./blog.py", dst+"blog.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the CLI.py to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"CLI.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./CLI.py", dst+"CLI.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the Markdown.py to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"Markdown.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./Markdown.py", dst+"Markdown.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy ".setup.sh" to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+".setup.sh'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./.setup.sh", dst+".setup.sh")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the "./templates" tree to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"templates'"+c.OKGREEN+" ... "+c.ENDC)
    copytree("./templates", dst+"templates")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "content" directory in the deployment folder
    if (not isdir(dst+"content")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"Content'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"content")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "html" directory in the deployment folder
    if (not isdir(dst+"html")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"html'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"html")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "html/assets" directory in the deployment folder
    if (not isdir(dst+"/html/assets")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"html/assets'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"html/assets")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the CSS file to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"html/assets/main.css'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./html/assets/main.css", dst+"html/assets/main.css")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

# Method: SanitizeDeploy
# Purpose: Sanitize FirstCrack files before deploying them publcily.
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def SanitizeDeploy(v=False):
    # Sanitize templates/index.html
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"templates/index.html'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"templates/index.html", "w").close()
    with open(dst+"templates/index.html", "a") as dst_fd:
        dst_fd.write("\n")
        dst_fd.write("<!-- DIVIDER -->\n")
        dst_fd.write("<p>\n    Example home page content.\n</p>")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Sanitize templates/projects.html
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"templates/projects.html'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"templates/projects.html", "w").close()
    with open(dst+"templates/projects.html", "a") as dst_fd:
        dst_fd.write('<!-- DIVIDER -->\n')
        dst_fd.write('<table style="width:100%;padding:20pt 0;" id="big_table">\n    <tbody>\n        <tr>\n            <td><a href="#academicWork">Academic Work</a></td>\n            <td><a href="#writingProjects">Writing Projects</a></td>\n            <td><a href="#codingProjects">Coding Projects</a></td>\n        </tr>\n    </tbody>\n</table>\n')
        dst_fd.write('<h1 class="headers" id="academicWork"><span><a href="#academicWork">#</a>&nbsp;</span>Academic Work</h1>\n<p>\n    This is an example section heading.\n</p>\n<h2 class="headers" id="capstone">Capstone<span>&nbsp;<a href="#capstone">#</a></span></h2>\n<p>\n    This is example section content.\n</p>\n')
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Sanitize templates/disclaimers.html
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"templates/disclaimers.html'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"templates/disclaimers.html", "w").close()
    with open("./templates/disclaimers.html", "r") as source_fd, open(dst+"templates/disclaimers.html", "a") as dst_fd:
        for line in source_fd:
            line = line.replace("Zachary Szewczyk", "{{full_name}}")
            dst_fd.write(line)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

# Method: GenExFiles
# Purpose: Create example files in the deployment directory
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def GenExFiles(v=False):
    with open(dst+"content/Test Original Article.txt", "w") as dst_fd:
        dst_fd.write("Test Original Article\n=====================\n\nThis is a test original article. Posts of this type appear with darker, non-underlined titles, and are truncated on the main page, archives page, and in the RSS feed.  \n\nStet posse an has, ut elit oratio nusquam mei, an eos posidonium concludaturque. Viris audiam voluptua ea duo, vis quod dolorem delicata et. Eos discere admodum an. Magna eligendi maluisset qui et. Ea nullam salutatus complectitur his, omnium omnesque ocurreret cum ad, quas impetus detracto qui ei. Mei mutat utamur tibique id, eum elitr tractatos voluptatum an.\n\nDiam graeco ei vis, equidem vivendo his ut. Eu lorem error iudico per, no iisque blandit necessitatibus nec. Ei velit tacimates sensibus sea. Vim meis consul urbanitas ea, choro laoreet verterem id usu, has alterum volumus scripserit ad. Sed expetenda gubergren ea, an nam integre pericula inciderint. Quodsi inciderint definitiones in sit, ea sea incorrupte sadipscing.\n\nSuas choro expetenda eum et. Wisi mucius iuvaret eu mel, pro harum euismod epicuri at. Cu qui praesent principes conclusionemque, ea ius vide intellegat, cibo nominati maluisset vis ad. Eum ei augue appareat invenire, minim discere inciderint usu eu. Blandit detracto deleniti ex duo, ad pro decore conceptam liberavisse. Ea sea sint ignota, te usu impetus consetetur. Mel aeterno inciderint an.\n\nNec hinc aliquando concludaturque in. Eos virtute suavitate et. Stet congue honestatis vis at, velit tantas at qui, homero habemus vituperata nec at. Ad cum dolores mentitum, no nam aperiam vivendum evertitur.")
    with open(dst+"content/Test Linkpost.txt", "w") as dst_fd:
        dst_fd.write("# [Test Linkpost](https://zacs.site/) #\n\nThis is a test linkpost. Posts of this type appear with lighter, underlined titles, and are not truncated displayed in full text on the main page, archives page, and in the RSS feed.  \n\nLorem ipsum dolor sit amet, his ad possim theophrastus comprehensam, illud tempor dolorum te quo. Quaerendum cotidieque id mel. Nam ne facer invidunt, discere reformidans nec id, vel adipiscing argumentum eu. Has et modus illum, simul mentitum ius ad, primis delenit interesset te quo.\n\nMel ea quaeque eripuit, has vidit probatus ocurreret no. Ius no alii verterem, ea vim legere vivendo, qui utinam tritani te. Ea sit quando tempor nemore. Ne justo prompta officiis nec, ea erant invenire principes his. Omnium noluisse at pri, novum utinam dolores et vel, ea altera tibique partiendo est. Hinc porro clita ut has.\n\nCum te debet volumus. Ius ne enim fugit exerci, everti invidunt perfecto sea ad. Oratio vocent praesent vel ex, quo odio definitiones id. Perfecto molestiae abhorreant an vix, sumo quaestio id mel, sed falli verterem et. Te omnium lucilius consectetuer mea.")
    utime(dst+"content/Test Linkpost.txt", (time()-10, time()-10))

# If run as as a standalone program ...
if (__name__ == "__main__"):
    # Detect if running in verbose mode
    if ("-v" in argv):
        verbose = True
    else:
        verbose = False

    # Clear deployment folder
    if (verbose): stdout.write(c.OKGREEN+"Clearing "+c.ENDC+"'"+dst+"'"+c.OKGREEN+" ... "+c.ENDC)
    for each in listdir(dst):
        if (each != ".git"): # Ignore git directory
            try:
                remove(dst+each)
            except:
                rmtree(dst+each)
    if (verbose): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy files to the deployment directory
    CopyToDeploy(verbose)
    SanitizeDeploy(verbose)
    GenExFiles(verbose)