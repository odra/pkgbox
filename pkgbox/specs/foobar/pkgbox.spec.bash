#!/bin/bash

pkgbox::pkg::depends "pkgbox-base"

pkgbox::pkg::prepare() {
    mkdir -p /etc/foobar
}

pkgbox::pkg::build() {
    touch /etc/foobar/build.lock
}

pkgbox::pkg::install() {
    echo 'foobar' > /etc/foobar/build.log
}

pkgbox::pkg::cleanup() {
   rm /etc/foobar/build.lock
}
