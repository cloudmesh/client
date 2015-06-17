doc:
	cd docs; Make html

tag:
	git tag
	@echo "New Tag?"; read TAG; git tag $$TAG; git push origin --tags

rmtag:
	git tag
	@echo "rm Tag?"; read TAG; git tag -d $$TAG; git push origin :refs/tags/$$TAG
