.PHONY: default
.PHONY: rebuild

default: EDITME
	./blog.py

rebuild:
	./blog.py -R

EDITME:
	@echo "First run. Creating EDITME"