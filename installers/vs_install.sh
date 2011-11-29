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
            echo "$prompt ERROR: configure command is not entered." >&1
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
    *)  echo "$prefix ERROR: $filename: unsupported extension." 2>&1
        return 1 ;;
    esac
    ## donwload
    local curl=`which curl`
    local wget=`which wget`
    if   [ -n "$curl" ]; then _cmd "curl -LO $url"  || return 1
    elif [ -n "$wget" ]; then _cmd "wget -N $url"   || return 1
    else
        echo "$prompt ERROR: 'curl' or 'wget' command required, but not installed." 2>&1
        return 1
    fi
    _cmd "$untar $filename"                       || return 1
    _cmd "cd $base/"                              || return 1
    ## compile and install
    _cmd "time nice -5 $configure"                || return 1
    _cmd "time nice -5 make"                      || return 1
    _cmd "time nice -5 make install"              || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which $bin"                             || return 1
    if [ "$prefix/bin/$bin" != `which $bin` ]; then
        echo "$prefix ERROR: $lang seems not installed correctly." 2>&1
        echo "$prefix exit 1" 2>&1
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
