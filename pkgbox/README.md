# Bash PoC

A small bash proof of concept to generate a valid runtime bundle to run builds with an
OCI runtime compliant implementation such as runc.

All commands are located in the "bin" folder and should be invoked from this directory.

## Dependencies

* crun: container runtime
* jq: oci json data manipulation

## PoC Findings

* Need a smart way to store layers additional metadata
  * Store layers in expected format while allowing users to pick layers to include in an exported image
* Some crun bindings are available upstream, but you need to build it yourself
* Replace rootfs generation with pulling images as "base boxes"
* Container file usage instead of dumb bash scripting
* The real deal will also need to properly handle OCI structs/types
* Simple web UI to showcase a "regisrty"?
