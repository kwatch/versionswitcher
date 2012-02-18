###
### This file will be imported by vs command after switching Python version.
###
#if [ -n "$pythonversion" ]; then
#    PS1="python-$pythonversion> "
#else
#    PS1="> "
#fi

pythonlib=$pythonroot/lib/python*
pythonsitelib=$pythonlib/site-packages

## python version
## (ex: 2.6, 2.7, 3.0, 3.1, 3.2, ...)
pyver=`python -c 'import sys;print("%s.%s"%sys.version_info[:2])'`

## edit python version in $PATH
## (ex. '/usr/local/python2.5/bin' => '/usr/local/python2.7/bin')
newpath=`echo $PATH | sed -e "s/python[0-9]\\.[0-9]/python$pyver/g"`
if [ "$PATH" != "$newpath" ]; then
    echo "$ export PATH=$newpath"
    export PATH=$newpath
    hash -r
fi
unset newpath

## edit python version in $PYTHONPATH
## (ex. '/usr/local/python2.5/lib' => '/usr/local/python2.7/lib')
if [ -n "$PYTHONPATH" ]; then
    newpypath=`echo $PYTHONPATH | sed -e "s/python[0-9]\\.[0-9]/python$pyver/g"`
    if [ "$PYTHONPATH" != "$newpypath" ]; then
        echo "$ export PYTHONPATH=$newpypath"
        export PYTHONPATH=$newpypath
    fi
    unset newpypath
fi

## edit python version in alias definition of 'easy_install'
## (see $HOME/.vs/misc/python.profile for detail)
has_alias=`alias | grep easy_install || true`
if [ -n "$has_alias" ]; then
    newdef=`alias easy_install | sed -e "s/python[0-9]\\.[0-9]/python$pyver/g"`
    if [ "$newdef" != `alias easy_install` ]; then
        echo "$ $newdef"
        eval "$newdef"
    fi
    unset newdef
fi
unset has_alias

## edit python version in alias definition of 'pip'
## (see $HOME/.vs/misc/python.profile for detail)
if [ -n "$PIP_INSTALL_OPTION" ]; then
    newopt=`echo $PIP_INSTALL_OPTION | sed -e "s/python[0-9]\\.[0-9]/python$pyver/g"`
    if [ "$PIP_INSTALL_OPTION" != "$newopt" ]; then
        echo "$ export PIP_INSTALL_OPTION=$newopt"
        export PIP_INSTALL_OPTION="$newopt"
    fi
    unset newopt
fi
