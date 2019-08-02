#!/usr/local/bin/python3

# Imports
from shutil import rmtree, copytree, copy # For directory and file operations
from os import mkdir, utime # To create directories
from os.path import isdir # To check for directories
from sys import argv, stdout, exit # Enable writing multiple times to the same line
from colors import c # For output styling
from time import sleep

# Target directory for public deployment
dst = "../Public/FirstCrack/"

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

    # Copy ".sys.sh" to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+".sys.sh'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./.sys.sh", dst+".sys.sh")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Clear the "system/*" tree in the deployment folder
    if (v): stdout.write(c.OKGREEN+"Clearing "+c.ENDC+"'"+dst+"system'"+c.OKGREEN+" ... "+c.ENDC)
    rmtree(dst+"system", ignore_errors=True)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the "./system" tree to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"system'"+c.OKGREEN+" ... "+c.ENDC)
    copytree("./system", dst+"system")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    # Copy "blog.py" dependencies to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"colors.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./colors.py", dst+"colors.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"ModTimes.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./ModTimes.py", dst+"ModTimes.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"Hash.py'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./Hash.py", dst+"Hash.py")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "Content" directory in the deployment folder
    if (not isdir(dst+"Content")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"Content'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"Content")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "local" directory in the deployment folder
    if (not isdir(dst+"local")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"local'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"local")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Create the "local/assets" directory in the deployment folder
    if (not isdir(dst+"/local/assets")):
        if (v): stdout.write(c.OKGREEN+"Creating "+c.ENDC+"'"+dst+"local/assets'"+c.OKGREEN+" ... "+c.ENDC)
        mkdir(dst+"local/assets")
        if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Copy the CSS file to the deployment folder
    if (v): stdout.write(c.OKGREEN+"Copying "+c.ENDC+"'"+dst+"local/assets/main.css'"+c.OKGREEN+" ... "+c.ENDC)
    copy("./local/assets/main.css", dst+"local/assets/main.css")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

# Method: SanitizeDeploy
# Purpose: Sanitize FirstCrack files before deploying them publcily.
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def SanitizeDeploy(v=False):
    # Sanitize blog.py
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"blog.py'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"blog.py", "w").close()
    with open("./blog.py", "r") as source_fd, open(dst+"blog.py", "a") as dst_fd:
        for line in source_fd:
            if (line[0:8] == "base_url"):
                line = line.replace("https://zacs.site", "YOUR BASE URL HERE")
            if (line[0:6] == "byline"):
                line = line.replace("Zac J. Szewczyk", "YOUR NAME HERE")
            if (line[0:21] == "    BuildFromTemplate"):
                temp = line.split('", ')
                temp.pop(3)
                temp.insert(3,'description="DESCRIPTION HERE')
                line = '", '.join(temp)
            dst_fd.write(line)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)
    
    # # Sanitize Markdown.py
    # if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"Markdown.py'"+c.OKGREEN+" ... "+c.ENDC)
    # open(dst+"Markdown.py", "w").close()
    # with open("./Markdown.py", "r") as source_fd, open(dst+"Markdown.py", "a") as dst_fd:
    #     for line in source_fd:
    #         if (line[0:21] == "path_to_content_files"):
    #             line = line.replace("zjszewczyk", "USERNAME_HERE")
    #         dst_fd.write(line)
    # if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Sanitize Markdown2.py
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"Markdown2.py'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"Markdown2.py", "w").close()
    with open("./Markdown2.py", "r") as source_fd, open(dst+"Markdown2.py", "a") as dst_fd:
        for line in source_fd:
            dst_fd.write(line)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Sanitize system/index.html
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"system/index.html'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"system/index.html", "w").close()
    with open(dst+"system/index.html", "a") as dst_fd:
        dst_fd.write("\n")
        dst_fd.write("<!-- DIVIDER -->\n")
        dst_fd.write("<p>\n    Example home page content.\n</p>")
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Sanitize system/projects.html
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"system/projects.html'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"system/projects.html", "w").close()
    with open(dst+"system/projects.html", "a") as dst_fd:
        dst_fd.write('<!-- DIVIDER -->\n')
        dst_fd.write('<table style="width:100%;padding:20pt 0;" id="big_table">\n    <tbody>\n        <tr>\n            <td><a href="#academicWork">Academic Work</a></td>\n            <td><a href="#writingProjects">Writing Projects</a></td>\n            <td><a href="#codingProjects">Coding Projects</a></td>\n        </tr>\n    </tbody>\n</table>\n')
        dst_fd.write('<h1 class="headers" id="academicWork"><span><a href="#academicWork">#</a>&nbsp;</span>Academic Work</h1>\n<p>\n    This is an example section heading.\n</p>\n<h2 class="headers" id="capstone">Capstone<span>&nbsp;<a href="#capstone">#</a></span></h2>\n<p>\n    This is example section content.\n</p>\n')
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

    # Sanitize system/disclaimers.html
    if (v): stdout.write(c.OKGREEN+"Writing "+c.ENDC+"'"+dst+"system/disclaimers.html'"+c.OKGREEN+" ... "+c.ENDC)
    open(dst+"system/disclaimers.html", "w").close()
    with open("./system/disclaimers.html", "r") as source_fd, open(dst+"system/disclaimers.html", "a") as dst_fd:
        for line in source_fd:
            if (line[0:20] == '    Zachary Szewczyk'):
                line = line.replace("Zachary Szewczyk", "Name here")
            dst_fd.write(line)
    if (v): stdout.write(c.OKGREEN+"done.\n"+c.ENDC)

# Method: GenExFiles
# Purpose: Create example files in the deployment directory
# Parameters:
# - v: Boolean that determines whether to print output or not. (Bool)
def GenExFiles(v=False):
    with open(dst+"Content/Test Original Article.txt", "w") as dst_fd:
        dst_fd.write("Test Original Article\n=====================\n\nThis is a test original article. Posts of this type appear with darker, non-underlined titles, and are truncated on the main page, archives page, and in the RSS feed.  \n\nStet posse an has, ut elit oratio nusquam mei, an eos posidonium concludaturque. Viris audiam voluptua ea duo, vis quod dolorem delicata et. Eos discere admodum an. Magna eligendi maluisset qui et. Ea nullam salutatus complectitur his, omnium omnesque ocurreret cum ad, quas impetus detracto qui ei. Mei mutat utamur tibique id, eum elitr tractatos voluptatum an.\n\nDiam graeco ei vis, equidem vivendo his ut. Eu lorem error iudico per, no iisque blandit necessitatibus nec. Ei velit tacimates sensibus sea. Vim meis consul urbanitas ea, choro laoreet verterem id usu, has alterum volumus scripserit ad. Sed expetenda gubergren ea, an nam integre pericula inciderint. Quodsi inciderint definitiones in sit, ea sea incorrupte sadipscing.\n\nSuas choro expetenda eum et. Wisi mucius iuvaret eu mel, pro harum euismod epicuri at. Cu qui praesent principes conclusionemque, ea ius vide intellegat, cibo nominati maluisset vis ad. Eum ei augue appareat invenire, minim discere inciderint usu eu. Blandit detracto deleniti ex duo, ad pro decore conceptam liberavisse. Ea sea sint ignota, te usu impetus consetetur. Mel aeterno inciderint an.\n\nNec hinc aliquando concludaturque in. Eos virtute suavitate et. Stet congue honestatis vis at, velit tantas at qui, homero habemus vituperata nec at. Ad cum dolores mentitum, no nam aperiam vivendum evertitur.")
    sleep(1)
    with open(dst+"Content/Test Linkpost.txt", "w") as dst_fd:
        dst_fd.write("# [Test Linkpost](https://zacs.site/) #\n\nThis is a test linkpost. Posts of this type appear with lighter, underlined titles, and are not truncated displayed in full text on the main page, archives page, and in the RSS feed.  \n\nLorem ipsum dolor sit amet, his ad possim theophrastus comprehensam, illud tempor dolorum te quo. Quaerendum cotidieque id mel. Nam ne facer invidunt, discere reformidans nec id, vel adipiscing argumentum eu. Has et modus illum, simul mentitum ius ad, primis delenit interesset te quo.\n\nMel ea quaeque eripuit, has vidit probatus ocurreret no. Ius no alii verterem, ea vim legere vivendo, qui utinam tritani te. Ea sit quando tempor nemore. Ne justo prompta officiis nec, ea erant invenire principes his. Omnium noluisse at pri, novum utinam dolores et vel, ea altera tibique partiendo est. Hinc porro clita ut has.\n\nCum te debet volumus. Ius ne enim fugit exerci, everti invidunt perfecto sea ad. Oratio vocent praesent vel ex, quo odio definitiones id. Perfecto molestiae abhorreant an vix, sumo quaestio id mel, sed falli verterem et. Te omnium lucilius consectetuer mea.")

# If run as as a standalone program ...
if (__name__ == "__main__"):
    # Detect if running in verbose mode
    if ("-v" in argv):
        verbose = True
    else:
        verbose = False

    # # Clear deployment directory if it exists
    # if (isdir(dst)):
    #     rmtree(dst)
    #     mkdir(dst)

    # Copy files to the deployment directory
    CopyToDeploy(verbose)
    SanitizeDeploy(verbose)
    GenExFiles(verbose)