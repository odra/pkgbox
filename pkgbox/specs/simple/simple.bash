#!/bin/bash

pkgbox::prep() {
    dnf install -y gcc make
    make prepare
}

pkgbox::build() {
    make build
}

pkgbox::install() {
    make install
}

pkgbox::cleanup() {
   make clean
}
