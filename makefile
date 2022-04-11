.PHONY: default # Default rule. Update site.
.PHONY: verbose # Update site, with verbose flag.
.PHONY: cli # Enter CLI
.PHONY: rebuild # Force rebuild entire site.
.PHONY: timestamp # Reconcile article and publication timestamps, and fix.
.PHONY: help # Display help menu
.PHONY: preview # Host local web server to preview local copy of website
.PHONY: public # Host public web server to preview local copy of website
.PHONY: deploy # Deploy to GitHub Pages, and generate a generic commit message.
.PHONY: pull # Pull changes from remote source control repository.

default: Config.json
	@./blog.py
verbose:
	@./blog.py -v
cli:
	@./blog.py -a
rebuild:
	@./blog.py -R --exit
timestamp:
	@./blog.py -r --exit
	
help:
	@echo "make default   - Default rule. Update site."
	@echo "make verbose   - Update site, with verbose output."
	@echo "make cli       - Enter the command line interface."
	@echo "make rebuild   - Force rebuild entire site."
	@echo "make timestamp - Make article and post publication timestamps match."
	@echo "make help      - Display this help menu."
	@echo ""
	@echo "make private   - Host local web server to preview local website."
	@echo "                 \033[1mNote:\033[0m this web server is only available to you."
	@echo "make public    - Host public web server to preview local website."
	@echo "                 \033[1mNote:\033[0m this web server is available to your entire network. Use"
	@echo "                 to view your local website on other devices, and with caution."
	@echo ""
	@echo "make deploy    - Deploy to GitHub Pages, and update source control."
	@echo "make pull      - Pull changes from remote source control repository."
	@echo ""

preview:
	@./blog.py -p --exit
public:
	@./blog.py -P --exit

deploy:
	@git add -A
	@git commit -m "Deployment commit on `date`"
	@make push
pull:
	@git subtree pull --prefix=html git@github.com:zacjszewczyk/zacjszewczyk.github.io.git master
	@git pull
push:
	@git subtree push --prefix=html git@github.com:zacjszewczyk/zacjszewczyk.github.io.git master
	@git push

Config.json:
	@echo "First run detected. Please enter the following information:"
	@chmod 700 ./.setup.sh
	@./.setup.sh
	@rm -f ./.setup.sh