Introduction
============

NOTE: this branch belong to a proof-of-concept work written in bash.

Pkgbox: manage package building as OCI Layers.

The idea of this project to build software and package them as OCI image layers
so those can be applied in a container or directly shipped into a system that is able
to apply/commit said layers.

Usage
-----

This section describe the basic usage of the tool.

This branch (bash-poc) introduces a proof of concept in bash (because why not) and all
commands should be executed from the **pkgbox** folder.

Last but not least, **PKGBOX_HOME** is the environtment variable used by the tool for all
its file operations and it will default to **/tmp/pkgbox**.

It's also woth noting that this branch may rely on some tools that are specific to a Fedora
linux distribution such as **dnf**.

Initialize pkgbox by running (requires sudo due to dnf usage):

.. code-block:: bash
   
   ./bin/pkgbox-init

The above command will create the **$PKGBOX_HOME** folder if it does not exist and
will create a basic rootfs located at **$PKGBOX_HOME/buildboxes/pkgbox-base** to be
used by other builds.

The next step is to create a "build spec", just for the sake of defining a simple way of
running the usual packaging tasks: **prepare/configure**, **build**, **archive/install** and **cleanup**.

We will be using a sample located at **specs/hello-world-c**, which will run the following obvious
tasks:

.. code-block:: bash

   #!/bin/bash

   pkgbox::depends pkgbox-base

   pkgbox::prepare() {
   }
   
   pkgbox::build() {
   }
   
   pkgbox::install() {
   }
   
   pkgbox::cleanup() {
   }
   
   if [ ! -z "$1" ]; then
       $1
   fi

The last lines of our "job definition" serve the purpose of running this file as an
executable one by passing one of those functions names as an argument.

The special function **pkgbox::depends $buildbox** can be invoked as many times as needed
and will apply the rootfs of each referenced build box in order before running any packaging
tasks.

The following command should be used to invoke a build:

.. code:: bash
   
   ./bin/pkgbox-build $SPEC_DIR $BOX_NAME

Where **SPEC_DIR** is the folder contaning the "spec file" definition and **BOX_NAME** the box directory
name to be used in **/tmp/pkgbox/buildboxes/$BOX_NAME**, box names should be unique.

Finally, you can export a box into an OCI layer archive by running:

.. code:: bash

   ./bin/pkgbox-export $BOX_NAME

This will generate an archive in your current working directory as **pkgbox-$BOX_NAME.tar.gz**.
