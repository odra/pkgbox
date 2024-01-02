#!/bin/bash

declare -f -F pkgbox::pkg::depends > /dev/null
if [ "$?" -eq 0 ]; then
  pkgbox::pkg::depends "pkgbox-base"
fi

pkgbox::pkg::prepare() {
    dnf \
      --releasever 39 \
      install -y gcc make

    make prepare
}

pkgbox::pkg::build() {
    make build
}

pkgbox::pkg::install() {
    make install
}

pkgbox::pkg::cleanup() {
   make clean
   dnf remove -y gcc make
}

if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
  (
    cd src;
    pkgbox::pkg::prepare;
    pkgbox::pkg::build;
    pkgbox::pkg::install;
    pkgbox::pkg::cleanup;
  )
fi
