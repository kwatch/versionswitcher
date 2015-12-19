#!/bin/sh

###
### $Release: 0.0.0 $
### $License: Public Domain $
###

_install_gauche() {
    local version=$1
    local prefix=$2
    local lang="gauche"
    local bin="gosh"
    local base="Gauche-$version"
    local filename="$base.tgz"
    #local url="http://ftp.jaist.ac.jp/pub/sourceforge/g/project/ga/gauche/Gauche/$filename"
    local url="http://prdownloads.sourceforge.net/gauche/$filename"
    local configure="./configure --prefix=$prefix"
    . $HOME/.vs/installers/vs_install.sh
    _generic_installer "$lang" "$bin" "$version" "$base" "$filename" "$url" "$prefix" "$configure"  || return 1
    ## finish
    local prompt='**'
    echo
    echo "$prompt Installation finished successfully."
    echo "$prompt   language:  $lang"
    echo "$prompt   version:   $version"
    echo "$prompt   directory: $prefix"
}

if [ -n "$1" -a -n "$2" ]; then
    if [ "root" = `whoami` ]; then
        echo "*** not allowed to execute by root user!" 1>&2
        echo "*** exit 1" 1>&2
        exit 1
    fi
    _install_gauche "$1" "$2"
fi
