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

_install_luajit() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="luajit"
    local prompt="**"
    ## donwload
    local base="LuaJIT-$version"
    local url="http://luajit.org/download/$base.tar.gz"
    _cmd "wget -N $url"                           || return 1
    _cmd "tar xzf $base.tar.gz"                   || return 1
    _cmd "cd $base/"                              || return 1
    ## compile and install
    _cmd "time make PREFIX=$prefix"               || return 1
    _cmd "time make install PREFIX=$prefix"       || return 1
    _cmd "cd .."                                  || return 1
    ## create a link of binary
    if [ ! -f "$prefix/bin/luajit" ]; then
        _cmd "(cd $prefix/bin; ln luajit-$version luajit)" || return 1
    fi
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which luajit"                           || return 1
    if [ "$prefix/bin/luajit" != `which luajit` ]; then
        echo "$prefix ERROR: luajit seems not installed correctly." 2>&1
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
    _install_luajit "$1" "$2"
fi
