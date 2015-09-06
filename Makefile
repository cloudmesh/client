UNAME := $(shell uname)

BROWSER=firefox
ifeq ($(UNAME), Darwin)
BROWSER=open
endif
ifeq ($(UNAME), Windows)
BROWSER=/cygdrive/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe
endif
ifeq ($(UNAME), CYGWIN_NT-6.3)
BROWSER=/cygdrive/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe
endif

test:
	echo $(UNAME)


doc: man
	cd docs; make html

publish:
	ghp-import -n -p docs/build/html

view:
	$(BROWSER) docs/build/html/index.html

man: cloudmesh
	cm man > docs/source/man/man.rst

cloudmesh:
	python setup.py install

log:
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push

######################################################################
# CLEANING
######################################################################

clean:
	cd docs; make clean
	rm -rf build dist docs/build .eggs *.egg-info
	rm -rf *.egg-info
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;
	echo "clean done"

######################################################################
# TAGGING
######################################################################

tag: log
	cm-authors > AUTHORS
	git tag
	@echo "New Tag?"; read TAG; git tag $$TAG; python setup.py install; git commit -m $$TAG --allow-empty; git push origin --tags

rmtag:
	git tag
	@echo "rm Tag?"; read TAG; git tag -d $$TAG; git push origin :refs/tags/$$TAG


