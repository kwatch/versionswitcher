##
## $Release: 0.0.0 $
## $Copyright: copyright(c) 2011-2012 kuwata-lab.com all rights reserved $
## $License: Public Domain $
##

##
## .profile for Python to create local environment, similar to virtualenv.
##
## What this file to do:
## * create local directories for Python library and script
## * set $PATH and $PYTHONPATH to include local directory
## * configure 'easy_install' and 'pip' commands to install packages into
##   local directory
##
## How to use:
##   ### create project directory
##   $ mkdir helloworld
##   $ cd helloworld/
##   ### (optional) create 'lib' and 'bin' directories
##   $ mkdir lib     # not necessary (but recommended)
##   $ mkdir bin     # not necessary (but recommended)
##   ### copy 'python.profile' as '.profile'
##   $ cp $HOME/.vs/misc/python.profile .profile
##   ### load it, and 'local' directory will be created
##   $ source .profile
##   $ ls -F local
##   bin/    lib/
##   ### $PYTHONPATH will include 'local' directory
##   $ echo $PYTHONPATH
##   /home/yourname/helloworld/lib:/home/yourname/helloworld/local/lib/python2.7/site-packages:/home/yourname/helloworld/local/lib/python
##   ### 'easy_install' will install packages into 'local' directory
##   $ easy_install pip
##   $ ls -Fd local/lib/python2.7/site-packages/pip*
##   local/lib/python2.7/site-packages/pip-1.1-py2.7.egg/
##   $ which pip
##   /home/yourname/helloworld/local/bin/python2.7/bin/pip
##   ### 'pip' will also install packages into 'local' directory
##   $ pip install tenjin
##   $ ls -Fd local/lib/python2.7/site-packages/tenjin*
##   local/lib/python2.7/site-packages/tenjin.py
##   local/lib/python2.7/site-packages/tenjin.pyc
##   $ which pytenjin
##   /home/yourname/helloworld/local/bin/python2.7/pytenjin
##

## helper function to add path into $PATH
function _append_to_path() {
    eval "_path=$1"
    case :$PATH: in
        *:$_path:*)
            ;;
        *)
            echo "export PATH=$1:\$PATH"
            export PATH=$_path:$PATH
            ;;
    esac
    unset _path
}

## detect python version (for example '2.7' or '3.2')
pyver=`python -c 'import sys;print("%s.%s"%sys.version_info[:2])'`

## create 'local/bin' and add it to $PATH
[ -d "local/bin" ] || mkdir -p "local/bin"
_append_to_path '$PWD/local/bin'
if [ -n "$VS_PATH" ]; then
    [ -d "local/bin/python$pyver" ] || mkdir -p "local/bin/python$pyver"
    _append_to_path '$PWD/local/bin/python'$pyver
fi

## add 'bin' to $PATH if exists
[ -d "$PWD/bin" ] && _append_to_path '$PWD/bin'

## create 'local/lib/python' directory when not exist
if [ ! -d "$PWD/local/lib/python" ]; then
    echo "mkdir -p \$PWD/local/lib/python"
    mkdir -p "$PWD/local/lib/python"
fi

## create 'local/lib/pythonX.X/site-packages' directory when not exist
sitedir="local/lib/python$pyver/site-packages"
if [ ! -d "$PWD/$sitedir" ]; then
    echo "mkdir -p \$PWD/$sitedir"
    mkdir -p "$PWD/$sitedir"
fi

## set $PYTHONPATH to include 'local/lib/python/site-packages' and 'lib'
if [ -d "lib" ]; then
    echo export "PYTHONPATH=\$PWD/lib:\$PWD/$sitedir:\$PWD/local/lib/python"
    export PYTHONPATH=$PWD/lib:$PWD/$sitedir:$PWD/local/lib/python
else
    echo export "PYTHONPATH=\$PWD:\$PWD/$sitedir\:$PWD/local/lib/python"
    export PYTHONPATH=$PWD:$PWD/$sitedir:$PWD/local/lib/python
fi
unset sitedir

## enforce 'easy_install' and 'pip' to install packages into 'local'
if [ -z "$VS_PATH" ]; then
    echo 'alias easy_install="\\easy_install --prefix=$PWD/local"'
    alias easy_install="\\easy_install --prefix=$PWD/local --script-dir=$PWD/local/bin/python$pyver"
    echo 'export PIP_INSTALL_OPTION="--prefix=$PWD/local"'
    export PIP_INSTALL_OPTION="--prefix=$PWD/local"
else
    echo 'alias easy_install="\\easy_install --prefix=$PWD/local --script-dir=$PWD/local/bin/python'$pyver'"'
    alias easy_install="\\easy_install --prefix=$PWD/local --script-dir=$PWD/local/bin/python$pyver"
    echo 'export PIP_INSTALL_OPTION="--prefix=$PWD/local --install-scripts=$PWD/local/bin/python"'$pyver'"'
    export PIP_INSTALL_OPTION="--prefix=$PWD/local --install-scripts=$PWD/local/bin/python$pyver"
fi
unset pyver
