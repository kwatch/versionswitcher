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
    _generic_installer "$lang" "$bin" "$version" "$base" "$filename" "$url" "$prefix" "$configure" || return 1
    ## install 'cpanm'
    local prompt='**'
    local script="cpanm"
    local script_path
    local input
    echo
    echo -n "$prompt Install '$script' command? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)
        url="http://cpanmin.us/"
        local curl=`which curl`
        local wget=`which wget`
        if [ -n "$curl" ]; then
            _cmd "curl -Lo $prefix/bin/$script $url" || return 1
        elif [ -n "$wget" ]; then
            _cmd "wget --no-check-certificate -O $prefix/bin/$script $url" || return 1
        else
            echo "$prompt ERROR: 'curl' or 'wget' command required, but not installed." 2>&1
            return 1
        fi
        _cmd "chmod a+x $prefix/bin/$script"         || return 1
        _cmd "which $script"                         || return 1
        script_path=`which $script`
        if [ "$script_path" != "$prefix/bin/$script" ]; then
            echo "$prompt ERROR: $script seems not installed correctly." 2>&1
            echo "$prompt exit 1" 2>&1
            return 1
        fi
        echo "$prompt $script installed successfully."
        ;;
    *)
        echo "$prompt skip to install $script command."
        ;;
    esac
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
    _install_perl "$1" "$2"
fi
