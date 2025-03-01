SHELL := /bin/bash
REG := localhost
NAME := pkgbox-box
TAG := latest
IMAGE := ${REG}/${NAME}:${TAG}
PODMAN_OPTS := 
BUILD_OPTS :=

.PHONY: build
build:
	podman ${PODMAN_OPTS} build ${BUILD_OPTS} -t ${IMAGE} .

.PHONY: create
create:
	toolbox create --image ${IMAGE} ${NAME}
