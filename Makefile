# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

PYTHON 			:= /usr/bin/env python
PYTHON_PIP  	:= /usr/bin/env pip

# Put it first so that "make" without argument is like "make help".
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-32s-\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install development extra dependencies.
	@echo "Installing development requirements..."
	@$(PYTHON_PIP) install -e .'[all]' -r requirements-tox.txt

test:  ## Run tox test.
	@echo "Running tox..."
	@pip freeze | grep -q -i 'tox' || $(PYTHON_PIP) install -r requirements-tox.txt
	@tox

deploy:  ## Release project to PyPI.
	@echo "Deploying to PyPI..."
	@pip freeze | grep -q -i 'twine' || $(PYTHON_PIP) install -U twine
	@$(PYTHON) setup.py sdist bdist_wheel
	@twine upload -r pypi dist/*

deploy-test:  ## Release project to PyPI test
	@echo "Deploying to PyPI test..."
	@pip freeze | grep -q -i 'twine' || $(PYTHON_PIP) install -U twine
	@$(PYTHON) setup.py sdist bdist_wheel
	@twine upload -r testpypi dist/*

changelog:  ## Generate a CHANGELOG.md file
	@echo "Generating CHANGELOG.md..."
	@which github_changelog_generator || gem install github_changelog_generator
	@github_changelog_generator -u lmcgartland -p graphene-file-upload

.PHONY: help install test deploy deploy-test changelog
