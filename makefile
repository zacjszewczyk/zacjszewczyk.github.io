.PHONY: default
.PHONY: rebuild
.PHONY: deploy

default: EDITME
	@./blog.py

rebuild:
	@./blog.py -R

deploy:
	@firebase deploy
	@git add .
	@git commit -m "New post deployed."
	@gp

EDITME:
	@echo "First run. Creating EDITME"