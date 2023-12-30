#!/bin/bash

pkgbox::prepare() {
    dnf --releasever 39 install -y gcc make
    make prepare
}

pkgbox::build() {
    make build
}

pkgbox::install() {
    make install
}

pkgbox::cleanup() {
   dnf remove -y gcc make
   make clean
}

if [ ! -z "$1" ]; then
    $1
fi
