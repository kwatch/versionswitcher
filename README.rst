======
README
======

:Release:    0.1.0
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


Installation
============

1. Download 'versionswitcher.sh'
2. Import it.
3. Set shell variable $VERSIONSWITCHER_PATH.

An example to install::

    $ mkdir ~/lib
    $ cd ~/lib
    $ url=http://github.com/kwatch/versionswitcher/raw/master
    $ wget --no-check-certificate $url/versionswitcher.sh
    $ . versionswitcher.sh
    $ VERSIONSWITCHER_PATH=$HOME/lang
    $ vs -h         # show help
    $ echo '. $HOME/lib/versionswitcher.sh'   >> ~/.bashrc
    $ echo 'VERSIONSWITCHER_PATH=$HOME/lang'  >> ~/.bashrc

All languages which you want to switch should be installed into $HOME/lang
(or other directory where you specified by $VERSIONSWITCHER_PATH) such as::

    + $HOME/
      + lang/
        + ruby/
          + 1.8.6-p369/
          + 1.8.7-p334/
          + 1.9.2-p378/
        + python/
          + 2.5.5/
          + 2.6.6/
          + 2.7.1/
          + 3.2.0/
        + node/
          + 0.4.2/
          + 0.4.7/

The following is an example to install Ruby 1.9.2 into $HOME/lang/ruby::

    $ wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.2-p180.tar.bz2
    $ tar xjf ruby-1.9.2-p180.tar.bz2
    $ cd ruby-1.9.2-p180/
    $ ./configure --prefix=$HOME/lang/ruby/1.9.2-p180
    $ JOBS=2 make
    $ make install
    $ vs ruby 1.9.2       # or vs ruby latest
    $ which ruby
    /home/yourname/lang/ruby/1.9.2-p378/bin/ruby
    $ which gem
    /home/yourname/lang/ruby/1.9.2-p378/bin/gem
    $ gem -v
    1.3.7
    $ gem update --system
    $ gem -v
    1.7.2

The following is an example to install Python 3.2 and distribute module into $HOME/lang/python::

    $ wget http://www.python.org/ftp/python/3.2/Python-3.2.tar.bz2
    $ tar xjf Python-3.2.tar.bz2
    $ cd Python-3.2/
    $ ./configure --prefix=$HOME/lang/python/3.2.0    # not '3.2'!
    $ JOBS=2 make
    $ make install
    $ (cd $HOME/lang/python/3.2.0/bin; ln python3.2 python)
    $ vs python 3.2       # or vs python latest
    $ which python
    /home/yourname/lang/python/3.2.0/bin/python
    $ wget http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py
    $ which easy_install
    /home/yourname/lang/python/3.2.0/bin/easy_install
    $ easy_install --version
    distribute 0.6.15
    $ easy_install readline     # for Mac OS X

The following is an example to install Node.js 0.4.7 into $HOME/lang/node::

    $ wget http://nodejs.org/dist/node-v0.4.7.tar.gz
    $ tar xzf node-v0.4.7.tar.gz
    $ cd node-v0.4.7/
    $ ./configure --prefix=$HOME/lang/node/0.4.7
    $ JOBS=2 make
    $ make test
    $ make install
    $ vs node 0.4.7       # or vs node latest
    $ which node
    /home/yourname/lang/node/0.4.7/bin/node
    $ node -v
    v0.4.7
    $ wget http://npmjs.org/install.sh
    $ sh install.sh
    $ which npm
    /home/yourname/lang/node/0.4.7/bin/npm
    $ npm -v
    0.3.18


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
