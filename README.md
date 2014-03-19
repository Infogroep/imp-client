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

Installation on Windows (8)
---------------------------
* Check out the imp-client and do the command as described above.
* Use pip (or easy_install) to install twisted:
    `pip install twisted`
    or
    `easy_install twisted`
* If the installation of twisted gives problem due to missing modules, install those first, or get them from: `http://www.lfd.uci.edu/~gohlke/pythonlibs/`
* Run imp-client by going to imp-client folder through command line and run:
    `python imp`
Note: The Python directory has to be added to the environment variable `PATH`.
* In order to run the imp-client by just typing `ìmp` from anywhere in the commandline following the instructions on this link: `http://stackoverflow.com/questions/4621255/how-do-i-run-a-python-program-in-the-command-prompt-in-windows-7`
or use follow these steps:

    1) Add .PY and .PYC to the environment variable `PATHEXT`. 
    
    2) Add the folder location of the imp-client to the environment variable `PATH`.
    
    3) If you have any command prompts open, close them and start command prompt again.
    
    4) Type: `imp`.

Installation on other systems
-----------------------------
* Install python2.7 and its development headers.
* Install pip: <http://www.pip-installer.org/en/latest/installing.html>
* Use pip to install twisted:
  `sudo pip-2.7 install twisted`
* Make a symlink in your bin folder: `sudo ln -s "<path-to-imp-git-checkout>/imp" /usr/local/bin/imp`
