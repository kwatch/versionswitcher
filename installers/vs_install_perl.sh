#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

_install_perl() {
    local version=$1
    local prefix=$2
    local lang="perl"
    local bin="perl"
    local base="perl-$version"
    local filename="$base.tar.bz2"
    local configure="./configure -d -Dprefix=$prefix"
    case "$version" in
    5.6.*|5.7.*|5.8.*|5.9.*|5.10.*)   filename="$base.tar.gz";;
    esac
    local url="http://www.cpan.org/src/5.0/$filename"
    . $HOME/.vs/installers/vs_install.sh
    _generic_installer "$lang" "$bin" "$version" "$base" "$filename" "$url" "$prefix" "$configure"
}

if [ -n "$1" -a -n "$2" ]; then
    if [ "root" = `whoami` ]; then
        echo "*** not allowed to execute by root user!" 2>&1
        echo "*** exit 1" 2>&1
        exit 1
    fi
    _install_perl "$1" "$2"
fi
