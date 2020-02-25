#
# This target is meant for use with versioneer only!!
# To install versioneer, see https://github.com/warner/python-versioneer
# It is very simple to install, use pep440. Once configured, you can
# use this target and greatly simplify publishing to PyPi or Artifactory!!
#
# By default, make release will:
#  - tag your current branch
#      $ make release bump=major
#      $ make release bump=minor
#      $ make release
#  - Publish your Python package to your PyPi repository with the new tag
#  - Perform a git push on any committed changes you have
#  - Perform a git push --tags to add the new tag to git
#
release:
	$(eval v := $(shell git describe --tags --abbrev=0 | sed -Ee 's/^v|-.*//'))
ifeq ($(bump), major)
	$(eval f := 1)
else ifeq ($(bump), minor)
	$(eval f := 2)
else
	$(eval f := 3)
endif
	git tag -a `echo $(v) | awk -F. -v OFS=. -v f=$(f) '{ $$f++ } 1'` && \
	git commit -am "Bumped to version `echo $(v) | awk -F. -v OFS=. -v f=$(f) '{ $$f++ } 1'`" || /bin/true
	git push --tags

clean:
	rm -f *.json *.yml *.xml *.lst *.csv
