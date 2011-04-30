======
README
======

:Release:    0.0.0
:Copyright:  copyright(c) 2011 kuwata-lab.com all rights reserved
:License:    Public Domain


About VersionSwitcher
=====================

VersionSwitcher is a small utility to switch version of programming language
or application. Switching mechanism is just modiying $PATH environment
variable, therefore it doesn't depend on a certain programming language
or application.

Features:

* Switch language version by modifying $PATH environment variable.
* Supports any programming languages such as Ruby, Python, Node.js, and
  so on (you don't have to change switcher tool for each language).

Currently it only supports bash and zsh on Unix-like system or Mac OS X.


Usage
=====

::

    $ . /some/where/to/versionswitcher.sh
    $ VERSIONSWITCHER_PATH=$HOME/lang
    $ vs python 2.6.6   # use $HOME/lang/python/2.6.6
    $ vs python 2       # use $HOME/lang/python/2.x.x (ex. 2.7.1)
    $ vs python latest  # use latest version under $HOME/lang/python
    $ vs python -       # use system-installed one (ex. /usr/bin/python)
    $ vs python         # show installed versions of python
    $ vs                # show all languages installed


Install VersionSwitcher
=======================

1. Download 'versionswitcher.sh' and import it.
2. Set shell variable $VERSIONSWITCHER_PATH.
3. Type 'vs -h' to show help message.

An example to install::

    $ wget http://versionswitcher.appspot.com/versionswitcher.sh
    $ . versionswitcher.sh
    $ VERSIONSWITCHER_PATH=$HOME/lang
    $ vs -h         # show help

And add settings to your ~/.bashrc or ~/.zshrc:

    $ dir=~/.versionswitcher
    $ mkdir $dir
    $ mv versionswitcher.sh $dir
    $ echo ". $dir/versionswitcher.sh"        >> ~/.bashrc
    $ echo 'VERSIONSWITCHER_PATH=$HOME/lang'  >> ~/.bashrc


Install Languages
=================

All languages which you want to switch should be installed into $HOME/lang
(or other directory where you specified by $VERSIONSWITCHER_PATH) such as::

    + $HOME/
      + lang/
        + ruby/
          + 1.8.7-p334/
	    + bin/
	      - ruby*
          + 1.9.2-p378/
	    + bin/
	      - ruby*
        + python/
          + 2.6.6/
	    + bin/
	      - python*
          + 2.7.1/
	    + bin/
	      - python*
          + 3.2.0/
	    + bin/
	      - python*
        + node/
          + 0.4.7/
	    + bin/
	      - node*

VersionSwitcher supports ANY programming languages to switch
as long as they are installed according to the above structure.

In addition, VersionSwitcher has a feature to install the following
languages easily::

* Ruby
* Python
* Node.js
* Lua
* LuaJIT

The following is an exaple to install Node.js (and npm command)::

    bash> vs -i
    ## try 'vs --install LANG' where LANG is one of:
    lua         # http://www.lua.org/
    luajit      # http://luajit.org/
    node        # http://nodejs.org/
    python      # http://www.python.org/
    ruby        # http://www.ruby-lang.org/
    bash> vs -i node
    ## try 'vs --install node VERSION' where VERSION is one of:
    0.4.7
    0.4.6
    0.4.5
    0.4.4
    bash> vs -i node latest    # or vs -i node 0.4.7
    ** latest version is 0.4.7
    ** Install into '/home/yourname/lang/node/0.4.7'. OK? [Y/n]: 
    ** Configure is './configure --prefix=/home/yourname/lang/node/0.4.7'. OK? [Y/n]: 
    $ wget -nc http://nodejs.org/dist/node-v0.4.7.tar.gz
    $ tar xzf node-v0.4.7.tar.gz
    $ cd node-v0.4.7/
    $ time ./configure --prefix=/home/yourname/lang/node/0.4.7
    ...(snip)...
    $ time JOBS=2 make
    ...(snip)...
    $ cd ..
    $ hash -r
    $ which node
    /home/yourname/lang/node/0.4.7/bin/node
    
    ** Install npm (Node Package Manger)? [Y/n]: 
    $ wget -qO - http://npmjs.org/install.sh | sh
    fetching: http://registry.npmjs.org/npm/-/npm-0.3.18.tgz
    0.4.7
    ! [ -d .git ] || git submodule update --init
    node cli.js cache clean
    ...(snip)...
    ** npm installed successfully.
    
    ** Installation is finished successfully.
    **   language:  node
    **   version:   0.4.7
    **   directory: /home/yourname/lang/node/0.4.7
    
    ** vs node 0.4.7
    $ export PATH=/home/yourname/lang/node/0.4.7/bin:/usr/local/bin:/usr/bin:/bin
    $ noderoot='/home/yourname/lang/node/0.4.7'
    $ nodeversion='0.4.7'
    $ which node
    /home/yourname/lang/node/0.4.7/bin/node

The above steps are same for other languages such as ruby, python, lua
and luajit.


Tips
====

* Short name 'vs' is an alias to function 'versionswitcher()'.

* It is allowed to set VERSIONSWITCHER_PATH=path1:path2:path3:...

* VersionSwitcher sets $xxxroot and $xxxversion shell variables.
  For example, if you execute 'vs ruby 1.9', $rubyroot and
  $rubyversion shell variables will be set.

* $HOME/.versionswitcher/hooks/<language>.sh is imported if exists.
  For example::

      ## $HOME/.versionswitcher/hooks/ruby.sh
      if [ -n "$rubyroot" ]; then
	  ## set prompt to show ruby version
	  PS1="ruby@$rubyversion> "
      else
	  ## clear prompt
	  PS1="> "
      fi


Changes
=======

Release 0.1.0 (2011-04-27)
    * Public release
