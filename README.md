imp-client
==========

IMP client

Checking out
============
Run the following commands:

    git clone https://github.com/Infogroep/imp-client.git
    cd imp-client
    git submodule init
    git submodule update


Installation
============

Installation on Linux Debian
----------------------------
Run install-deps

Installation on other systems
-----------------------------
* Install python2.7 and its development headers.
* Install pip: <http://www.pip-installer.org/en/latest/installing.html>
* Use pip to install twisted:
  `sudo pip-2.7 install twisted`
* Make a symlink in your bin folder: `sudo ln -s "<path-to-imp-git-checkout>/imp" /usr/local/bin/imp`
