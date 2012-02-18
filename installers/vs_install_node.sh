#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011-2012 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


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
            echo "$prompt ERROR: configure command is not entered." 1>&2
            return 1
        fi
        ;;
    esac
    ## donwload, compile and install
    local base="node-v$version"
    local url="http://nodejs.org/dist/v$version/$base.tar.gz"
    local nice="nice -10"
    case "$version" in
    0.5.0|0.4*|0.3*|0.2*|0.1*|0.0*)
        url="http://nodejs.org/dist/$base.tar.gz"
        ;;
    esac
    if [ ! -e "$base.tar.gz" ]; then
        local down=`_downloader "-LRO" ""`        || return 1
        _cmd "$down $url"                         || return 1
    fi
    _cmd "$nice tar xzf $base.tar.gz"             || return 1
    _cmd "cd $base/"                              || return 1
    _cmd "time $nice $configure"                  || return 1
    _cmd "time JOBS=2 $nice make"                 || return 1
    _cmd "time $nice make install"                || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which node"                             || return 1
    if [ "$prefix/bin/node" != `which node` ]; then
        echo "$prefix ERROR: node command seems not installed correctly." 1>&2
        echo "$prefix exit 1" 1>&2
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
        local down=`_downloader "-LRO" "-N"`      || return 1
        _cmd "$down http://npmjs.org/install.sh"  || return 1
        _cmd "sh install.sh"                      || return 1
        local npm_path=`which npm`
        if [ "$npm_path" != "$prefix/bin/npm" ]; then
            echo "$prompt ERROR: npm command seems not installed correctly." 1>&2
            echo "$prompt exit 1" 1>&2
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
        echo "*** not allowed to execute by root user!" 1>&2
        echo "*** exit 1" 1>&2
        exit 1
    fi
    _install_node "$1" "$2"
fi
