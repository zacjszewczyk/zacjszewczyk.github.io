# PHONY declarations
## default - Update the website.
## author  - Enter First Crack's "Authoring" mode.
## rebuild - Rebuild all structure files.
## deploy  - Deploy with Google Firebase, and commit changes
##           to remote source control repository.
## help    - Display the help menu.
.PHONY: default
.PHONY: author
.PHONY: rebuild
.PHONY: deploy
.PHONY: help

# Rule: default
# Purpose: Update the website.
# Prerequisites:
# - .config: Create the hidden config file on first run.
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
	-@firebase deploy 2> /dev/null || echo "No Firebase deployment found: "`date`
	-@(git add . 2> /dev/null && git commit -m "Deployment commit on "`date` && git push) || echo "No local repo found: "`date`

# Rule: help
# Purpose: Display the help menu.
# Prerequisites: none
help:
	@echo $help_menu

# Rule: .config
# Purpose: On first run, 1) Display help menu, and
#          2) create hidden config file.
# Prerequisites: none
.config:
	@echo "Welcome to First Crack."
	@echo
	@echo "This menu will appear until you finish setting up your website. After that, you can access it at again at any time with the command 'make help'." 
	@echo
	@echo $help_menu
	@echo
	@echo "First Crack will now prompt you to create the config file.
	@echo
