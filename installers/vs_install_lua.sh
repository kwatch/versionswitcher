#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_lua() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="lua"
    local prompt="**"
    ## detect platform
    local uname=`uname`
    local platform
    case "$uname" in
    Linux|linux)       platform='linux';;
    FreeBSD|freebsd)   platform='freebsd';;
    *BSD|*bsd)         platform='bsd';;
    Darwin|darwin)     platform='macosx';;
    *)                 platform='posix';;         # or 'generic'
    esac
    ## donwload
    local base="lua-$version"
    local url="http://www.lua.org/ftp/$base.tar.gz"
    if [ ! -e "$base.tar.gz" ]; then
        local down=`_downloader "-LRO" ""`        || return 1
        _cmd "$down $url"                         || return 1
    fi
    _cmd "tar xzf $base.tar.gz"                   || return 1
    _cmd "cd $base/"                              || return 1
    ## confirm platform
    local input
    echo "$prompt Available platform list is:"
    echo -n "$prompt "; make | grep linux
    echo -n "$prompt Detected platform is '$platform'. OK? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*) ;;
    *)
        echo -n "$prompt Enter platform: "
        read platform
        if [ -z "$platform"]; then
            echo "$prompt ERROR: platform is not entered." 1>&2
            return 1
        fi
        ;;
    esac
    ## compile and install
    local nice="nice -10"
    _cmd "time $nice make $platform"           || return 1
    _cmd "time $nice make install INSTALL_TOP=$prefix"  || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which lua"                              || return 1
    if [ "$prefix/bin/lua" != `which lua` ]; then
        echo "$prefix ERROR: lua seems not installed correctly." 1>&2
        echo "$prefix exit 1" 1>&2
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
        echo "*** not allowed to execute by root user!" 1>&2
        echo "*** exit 1" 1>&2
        exit 1
    fi
    _install_lua "$1" "$2"
fi
