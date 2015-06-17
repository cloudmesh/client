UNAME := $(shell uname)

BROWSER=firefox
ifeq ($(UNAME), Darwin)
BROWSER=open
endif
ifeq ($(UNAME), Windows)
BROWSER=firefox
endif



doc:
	cd docs; Make html

tag:
	git tag
	@echo "New Tag?"; read TAG; git tag $$TAG; git push origin --tags

rmtag:
	git tag
	@echo "rm Tag?"; read TAG; git tag -d $$TAG; git push origin :refs/tags/$$TAG

publish:
	ghp-import -n -p docs/build/html

view:
	$(BROWSER) docs/build/html/index.html


