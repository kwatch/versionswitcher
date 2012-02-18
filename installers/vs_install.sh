#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011-2012 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

_cmd() {
    echo '$' $1
    if eval $1; then
        return 0
    else
        echo "** FAILED: $1" 1>&2
        return 1
    fi
}

_downloader() {
    local curlopt=$1
    local wgetopt=$2
    local curl=`which curl`
    local wget=`which wget`
    local down
    if   [ -n "$curl" ]; then
        echo "curl $curlopt"
    elif [ -n "$wget" ]; then
        echo "wget $wgetopt"
    else
        echo "$prompt ERROR: 'wget' or 'curl' required." 1>&2
        return 1
    fi
}

_generic_installer() {
    ## arguments and variables
    local lang=$1
    local bin=$2
    local version=$3
    local base=$4
    local filename=$5
    local url=$6
    local prefix=$7
    local configure=$8
    local prompt="**"
    ## confirm configure option
    echo -n "$prompt Configure is '$configure'. OK? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*) ;;
    *)
        echo -n "$prompt Enter configure command: "
        read configure
        if [ -z "$configure"]; then
            echo "$prompt ERROR: configure command is not entered." 1>&2
            return 1
        fi
        ;;
    esac
    ## extension
    local untar
    case $filename in
    *.tar.gz)   untar="tar xzf";;
    *.tgz)      untar="tar xzf";;
    *.tar.bz2)  untar="tar xjf";;
    *.tbz)      untar="tar xjf";;
    *.zip)      untar="unzip";;
    *)  echo "$prefix ERROR: $filename: unsupported extension." 1>&2
        return 1 ;;
    esac
    ## donwload
    if [ ! -e "$filename" ]; then
        local down=`_downloader "-LRO" ""`        || return 1
        _cmd "$down $url"                         || return 1
    fi
    _cmd "$untar $filename"                       || return 1
    _cmd "cd $base/"                              || return 1
    ## compile and install
    local nice="nice -10"
    _cmd "time $nice $configure"                  || return 1
    _cmd "time $nice make"                        || return 1
    _cmd "time $nice make install"                || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which $bin"                             || return 1
    if [ "$prefix/bin/$bin" != `which $bin` ]; then
        echo "$prefix ERROR: $lang seems not installed correctly." 1>&2
        echo "$prefix exit 1" 1>&2
        return 1
    fi
    ## finish
    #echo
    #echo "$prompt Installation is finished successfully."
    #echo "$prompt   language:  $lang"
    #echo "$prompt   version:   $version"
    #echo "$prompt   directory: $prefix"
    return 0
}
