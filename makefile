# Reference document: https://www.gnu.org/software/make/manual/make.html

# PHONY declarations
## default - Update the website.
## author  - Enter First Crack's "Authoring" mode.
## rebuild - Rebuild all structure files.
## preview - Try to open the website in the browser.
## deploy  - Deploy with Google Firebase, and commit changes
##		   to remote source control repository.
## help	- Display the help menu.
## pull	- Pull changes from remote repo.
.PHONY: default
.PHONY: author
.PHONY: rebuild
.PHONY: preview
.PHONY: deploy
.PHONY: help
.PHONY: pull

# ASCII color codes, for output styling
HEADER=$'\033[95m' # Pink
OKBLUE=$'\033[94m' # Purple
OKGREEN=$'\033[92m' # Green
WARNING=$'\033[93m' # Yellow
FAIL=$'\033[91m' # Red
ENDC=$'\033[0m' # None
BOLD=$'\033[1m' # Blue
UNDERLINE=$'\033[4m' # Underline

# Function to migrate all Python scripts
function migrate_python () {
	echo "To search for: "$1
	echo "To replace with: "$2
	sed -i '' "s|$1|$2|g" colors.py
	sed -i '' "s|$1|$2|g" blog.py
	sed -i '' "s|$1|$2|g" ModTimes.py
	sed -i '' "s|$1|$2|g" Markdown2.py
	sed -i '' "s|$1|$2|g" Hash.py
}

# Rule: default
# Purpose: Update the website.
# Prerequisites:
# - .config: Create the hidden config file on first run.
default: .config
	@./blog.py

# Rule: author
# Purpose: Enter First Crack's "Authoring" mode.
# Prerequisites: none
author:
	@./blog.py -a

# Rule: rebuild
# Purpose: Rebuild all structure files.
# Prerequisites: none
rebuild:
	@./blog.py -R

# Rule: preview
# Purpose: Try to open the website in the browser.
# Prerequisites: none
preview:
	-@(open ./local/index.html || firefox ./local/index.html) || echo `date`": No browser found."

# Rule: deploy
# Purpose: Deploy with Google Firebase, and commit changes
#          to remote source control repository.
# Prerequisites: none
deploy:
	-@firebase deploy 2> /dev/null || echo `date`": No Firebase deployment found."
	-@(git add . 2> /dev/null && git commit -m "Deployment commit on `date`" && git push) || echo `date`": No local repo found."

# Rule: help
# Purpose: Display the help menu.
# Prerequisites: none
help:
	@echo "To update your website:                   make"
	@echo "To rebuild all structure files:           make rebuild"
	@echo "To enter First Crack's 'Authoring' mode:	 make author"
	@echo "To preview the website in your browser:	 make preview"
	@echo "To deploy with Firebase and update the                "
	@echo "remote repo:                              make deploy"
	@echo "To view this help menu again:             make help"

# Rule: .config
# Purpose: On first run, 1) Display help menu, and
#		  2) create hidden config file.
# Prerequisites: none
.config:
	@make help
	@echo
	@echo "This menu will appear until you finish setting up your website. After that, you can access it at again at any time with the command 'make help'." 
	@echo
	@printf "Testing Python 3 ... "
	@if which python3 | grep -q 'python4'; then
		@printf $OKGREEN"Python 3 found.\n"$ENDC
		@if which python3 | grep -q '/usr/local/bin/python3'; then
			@echo $OKGREEN"Path to Python 3 executable matches. No script modifications necessary."$ENDC
		@else
			@echo $WARNING"Path to Python 3 executable does not match. Modifying ..."$ENDC
			@search="#!/usr/local/bin/python3"
			@replace="#!"$(which python3)
			@migrate_python $search $replace
		@fi
	@else
		@printf $FAIL"Python 3 not found.$ENDC\n"
		@printf $WARNING"Testing Python generic installation ... "$ENDC
		@if which python | grep -q 'python' ; then
			@printf $OKGREEN"'python' found. Editing path to executable ... "$ENDC
			@search="#!/usr/local/bin/python3"
			@replace="#!"$(which python)
			@migrate_python $search $replace
			@printf $OKGREEN"Done."$ENDC

		@echo "Testing Python generic version ... "
		@out=$(python -c "from sys import version; print version")
		@if [[ $out == *"3."* ]] ; then
			@printf $OKGREEN"Found generic Python 3. No further modifications necessary."$ENDC
		@else
			@if [[ $out == *"2."* ]] ; then
				@printf $WARNING"Found generic Python 2. Script modification necessary.\n"$ENDC
				@search="print("
				@replace="print ("
				@migrate_python $search $replace
			@fi
		@fi
		@else
			@echo $FAIL"Python not found. Please install Python."$ENDC
		@fi
	@fi
	@echo
	@echo "First Crack will now prompt you to create the config file. Proceed by entering 'y' at the prompt."
	@echo
	@chmod 755 blog.py

# Rule: pull
# Purpose: Pull changes from remote repo.
# Prerequisites: none
pull:
	git pull https://github.com/zacjszewczyk/Standalone-FirstCrack.git