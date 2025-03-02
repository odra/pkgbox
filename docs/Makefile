SHELL := /bin/bash
.DEFAULT_GOAL := all

.PHONY: html
html:
	sphinx-build -M html source/ build/

.PHONY: clean
clean:
	rm -rf build/

.PHONY: all
all: clean html
