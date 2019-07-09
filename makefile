# PHONY declarations
## default - 
## author  - 
## rebuild -
## deploy  -
.PHONY: default
.PHONY: author
.PHONY: rebuild
.PHONY: deploy

# Rule: default
# Purpose: Update the website.
# Prerequisites:
# - EDITME: Create the config file on first run.
default: EDITME
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

# Rule: deploy
# Purpose: Deploy with Google Firebase, and commit changes
#          to remote source control repository.
# Prerequisites: none
deploy:
	@firebase deploy || echo "No Firebase deployment found."
	-@(git add . 2> /dev/null && git commit -m "Deployment commit on "`date` && git push) || echo "No local repo found: "`date`

# Rule: EDITME
# Purpose: Create the config file on first run.
# Prerequisites: none
EDITME:
	@echo "First run. Creating EDITME"
