#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_rubinius() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang='rubinius'
    local prompt="**"
    ## platform-specific settings
    local kind="source"
    local input
    case `uname` in
    Darwin|darwin)
        echo    "$prompt Which one do you want?"
        echo    "$prompt   1. Source code (and compile it)"
        echo    "$prompt   2. Binary package for Mac OS X 10.6"
        echo    "$prompt   3. Binary package for Mac OS X 10.5"
        echo    "$prompt   (NOTICE: versionswitcher can install binary packages,"
        echo    "$prompt            but can't support switching to them."
        echo    "$prompt            If you want siwtch by 'vs rubinius VERSION', select 1.)"
        echo -n "$prompt Select [1]: "
        read input; [ -z "$input" ] && input="1"
        case "$input" in
        1)  kind="source";;
        2)  kind="10.6.pkg";;
        3)  kind="10.5.pkg";;
        *)  echo "$prompt ERROR: unexpected value." 2>&1
            echo "$prompt exit 1." 2>&1
            return 1
            ;;
        esac
        ;;
    esac
    ## confirm configure option
    local input
    local configure="./configure --prefix=$prefix"
    if [ "$kind" = "source" ]; then
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
    fi
    ##
    #http://asset.rubini.us/rubinius-1.2.3-20110315.tar.gz
    #http://asset.rubini.us/rubinius-1.2.3-10.6.pkg.zip
    #http://asset.rubini.us/rubinius-1.2.3-10.5.pkg.zip
    local date
    if [ "$kind" = "source" ]; then
        case $version in
        1.2.3)  date='20110315' ;;
        *)  echo "$prompt ERROR: version $version is not supported to install." 2>&1
            return 1
            ;;
        esac
    fi
    ## donwload, compile and install
    local base
    local siteurl="http://asset.rubini.us"
    if [ "$kind" = "source" ]; then
        base="rubinius-$version-$date"
        if [ ! -e "$base.tar.gz" ]; then
            local down=`__vs_downloader "-LRO" ""`  || return 1
            _cmd "$down $url"                       || return 1
        fi
        _cmd "rm -rf rubinius-$version"           || return 1
        _cmd "tar xzf $base.tar.gz"               || return 1
        _cmd "cd rubinius-$version/"              || return 1
        _cmd "unset RUBYLIB"                      || return 1
        _cmd "time $configure"                    || return 1
        _cmd "time rake install"                  || return 1
        _cmd "cd .."                              || return 1
    else
        base="rubinius-$version-$kind"
        if [ ! -e "$base.zip" ]; then
            local down=`__vs_downloader "-LRO" ""`  || return 1
            _cmd "$down $url"                       || return 1
        fi
        _cmd "rm -rf $base"                       || return 1
        _cmd "unzip -q $base.zip"                 || return 1
        _cmd "open $base"                         || return 1
        ## finish
        echo
        echo "$prompt Install binary package according to installer."
        echo "$prompt Finish."
        return 0
    fi
    ## verify
    local command="rbx"
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which $command"                         || return 1
    if [ "$prefix/bin/$command" != `which $command` ]; then
        echo "$prompt failed: $command command seems not installed correctly." 2>&1
        echo "$prompt exit 1" 2>&1
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
        echo "$prompt not allowed to execute by root user!" 2>&1
        echo "$prompt exit 1" 2>&1
        exit 1
    fi
    _install_rubinius "$1" "$2"
fi
