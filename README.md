# HOME-interface

## Installation

Install python 3.6, other versions might work but are not tested. Python 2 will not work.

Install a virtual environment handler, I recommend virtualenvwrapper. Virtualenvwrapper is also used for start scripts, so using the base virtual env handling will result in you having to start things manually. The created virtual env should be named hint for start scripts to work.

```mkvirtualenv hint```

Install requirements from requirements.txt.

```pip install -r requirements.txt```

Install requirements for Angular.

```./install.sh```

The installation script is re-runnable if you need to upgrade any of the installed ```node_modules```. Note that the installation script will remove the entirety of the node_modules directory and reinstall from ```package.json```. The installation script will also clear the globally installed version of the Angular cli tool, so if you have another project depending on a specific version of Angular cli, you're better of installing manually with ```npm install```.

Install redis-server, this will be used as a websocket backend for django channels 2. Installation depends on your OS and distribution.
