#!/bin/sh

###
### $Release: 0.0.0 $
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

_install_gauche() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="gauche"
    local prompt="**"
    ## confirm configure option
    local configure="./configure --prefix=$prefix"
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
    ## donwload
    local base="Gauche-$version"
    local url="http://ftp.jaist.ac.jp/pub/sourceforge/g/project/ga/gauche/Gauche/$base.tgz"
    _cmd "wget -N $url"                           || return 1
    _cmd "tar xzf $base.tgz"                      || return 1
    _cmd "cd $base/"                              || return 1
    ## compile and install
    _cmd "time $configure"                        || return 1
    _cmd "time make"                              || return 1
    _cmd "time make install"                      || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which gosh"                             || return 1
    if [ "$prefix/bin/gosh" != `which gosh` ]; then
        echo "$prefix ERROR: Gauche seems not installed correctly." 2>&1
        echo "$prefix exit 1" 2>&1
        return 1
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
    _install_gauche "$1" "$2"
fi
