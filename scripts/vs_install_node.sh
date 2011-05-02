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

_install_node() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="node"
    local prompt="**"
    ## confirm configure option
    local input
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
    ## donwload, compile and install
    local base="node-v$version"
    local url="http://nodejs.org/dist/$base.tar.gz"
    _cmd "wget -N $url"                           || return 1
    _cmd "tar xzf $base.tar.gz"                   || return 1
    _cmd "cd $base/"                              || return 1
    _cmd "time $configure"                        || return 1
    _cmd "time JOBS=2 make"                       || return 1
    _cmd "time make install"                      || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which node"                             || return 1
    if [ "$prefix/bin/node" != `which node` ]; then
        echo "$prefix ERROR: node command seems not installed correctly." 2>&1
        echo "$prefix exit 1" 2>&1
        return 1
    fi
    ## install 'npm' (Node Package Manager)
    echo
    echo -n "$prompt Install npm (Node Package Manger)? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)
        #_cmd "curl http://npmjs.org/install.sh | sh" || return 1
        #_cmd "wget -qO - http://npmjs.org/install.sh | sh" || return 1
        _cmd "wget -N http://npmjs.org/install.sh" || return 1
        _cmd "sh install.sh"                    || return 1
        local npm_path=`which npm`
        if [ "$npm_path" != "$prefix/bin/npm" ]; then
            echo "$prefix ERROR: npm command seems not installed correctly." 2>&1
            echo "$prefix exit 1" 2>&1
            return 1
        fi
        echo "$prompt npm installed successfully."
        ;;
    *)
        echo "$prompt skip to install npm."
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
    _install_node "$1" "$2"
fi
