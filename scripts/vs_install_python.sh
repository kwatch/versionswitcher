#!/bin/sh

###
### $Date: $
### $Copyright: copyright(c) 2011 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

_cmd() {
    echo '$' $1
    if eval $1; then
        return 0
    else
        echo "** FAILED: $1" 2>&1
        return 1
    fi
}

_install_python() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="python"
    local prompt="**"
    local flags=""
    ## platform-specific settings
    local macports_patch_url=""
    local readline_required=""
    local pythonver=""
    local platform=`uname`
    local input
    case "$platform" in
    Darwin*|darwin*)
        ## require macports patch?
        case "$version" in
        2.4*)  pythonver="python24";;
        2.5*)  pythonver="python25";;
        esac
        if [ -n "$pythonver" ]; then
            macports_patch_url="http://svn.macosforge.org/repository/macports/trunk/dports/lang/$pythonver"
            local svnpath=`which svn`
            if [ -z "$svnpath" ]; then
                echo "$prompt ERROR: you must install Subversion to apply MacPorts patch for Python $pythonver. Try 'sudo port install subversion' at first." 2>&1
                return 1
            fi
        fi
        ## require libreadline?
        if [ -n "$pythonver" ]; then
            if [ -f "/opt/local/lib/libreadline.dylib" ]; then
                flags="CPPFLAGS=-I/opt/local/include LDFLAGS=-L/opt/local/lib "
            elif [ -f "/usr/local/lib/libreadline.dylib" ]; then
                flags=""
            else
                echo "$prompt On Mac OS X, it is recommended to install readline library'"
                echo "$prompt by 'sudo port install readline'. Stop install? [Y/n]: "
                read input;  [ -z "$input" ] && input="y"
                case $input in
                y*|Y*)
                    echo "$prompt Installation process is stopped."
                    return 1
                    ;;
                esac
                flags=""
            fi
        else
            readline_required="YES"
        fi
        ;;
    esac
    ## confirm configure option
    local configure="${flags}./configure --prefix=$prefix"
    echo -n "$prompt Configure is '$configure'. OK? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*) ;;
    *)
        echo -n "$prompt Enter configure command: "
        read configure
        if [ -z "$configure"]; then
            echo "$prompt ERROR: configure command is not entered." >&1
            return 1
        fi
        ;;
    esac
    ## donwload, compile and install
    local ver=`echo $version | sed 's/\.0$//'`
    local base="Python-$ver"
    local url="http://www.python.org/ftp/python/$ver/$base.tar.bz2"
    _cmd "wget -nc $url"                          || return 1
    _cmd "rm -rf $base"                           || return 1
    _cmd "tar xjf $base.tar.bz2"                  || return 1
    _cmd "cd $base/"                              || return 1
    if [ -n "$macports_patch_url" ]; then
        _cmd "svn checkout $macports_patch_url"   || return 1
        for i in $pythonver/files/patch-*.diff; do
            _cmd "patch -p0 < $i"                 #|| return 1
        done
    fi
    _cmd "time $configure"                        || return 1
    _cmd "time make"                              || return 1
    local make_target
    case $version in
    2*)  make_target="install";;
    3*)  make_target="fullinstall";;
    esac
    _cmd "time make $make_target"                 || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which python"                           || return 1
    if [ "$prefix/bin/python" != `which python` ]; then
        echo "$prefix ERROR: python command seems not installed correctly." 2>&1
        echo "$prefix exit 1" 2>&1
        return 1
    fi
    ## install 'easy_install'
    local easy_install_path
    local script='distribute_setup.py'
    echo
    echo -n "$prompt Install 'easy_install' command? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)
        url="http://python-distribute.org/$script"
        _cmd "wget -nc $url"                      || return 1
        _cmd "$prefix/bin/python $script"         || return 1
        _cmd "which easy_install"                 || return 1
        easy_install_path=`which easy_install`
        if [ "$easy_install_path" != "$prefix/bin/easy_install" ]; then
            echo "$prefix ERROR: easy_install command seems not installed correctly." 2>&1
            echo "$prefix exit 1" 2>&1
            return 1
        fi
        echo "$prompt easy_install command installed successfully."
        ;;
    *)
        echo "$prompt skip to install easy_install command."
        ;;
    esac
    ## install 'readline' package (for Mac OS X)
    if [ -n "$readline_required" -a -n "$easy_install_path" ]; then
        echo
        echo -n "$prompt Install 'readline' package? (recommended) [Y/n]: "
        read input;  [ -z "$input"] && input="y"
        case "$input" in
        y*|Y*)
            _cmd "easy_install readline"          || return 1
            ;;
        *)
            echo "$prompt skip to install readline package."
            ;;
        esac
    fi
    ## finish
    echo
    echo "$prompt Installation is finished successfully."
    echo "$prompt   language:  $lang"
    echo "$prompt   version:   $version"
    echo "$prompt   directory: $prefix"
}


if [ -n "$1" -a -n "$2" ]; then
    if [ "root" = `whoami` ]; then
        echo "*** not allowed to execute by root user!" 2>&1
        echo "*** exit 1" 2>&1
        exit 1
    fi
    _install_python "$1" "$2"
fi
