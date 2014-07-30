#!/bin/sh

###
### $Release: 0.0.0 $
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
    ## check compiler (g++) and rake command
    if [ "$kind" == "source" ]; then
        local gpp_path=`which g++`
        if [ -z "$gpp_path" ]; then
            echo "$prompt ERROR: g++ not installed. you must install 'g++' to compile Rubinius." 1>&2
            echo "$prompt exit 1." 1>&2
            return 1
        fi
        local rake_path=`which rake`
        if [ -z "$rake_path" ]; then
            echo "$prompt ERROR: rake not installed. you must install 'rake' to compile Rubinius." 1>&2
            echo "$prompt exit 1." 1>&2
            return 1
        fi
    fi
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
                echo "$prompt ERROR: configure command is not entered." 1>&2
                return 1
            fi
            ;;
        esac
    fi
    ## donwload, compile and install
    local base
    local siteurl="http://releases.rubini.us"
    local url
    local nice="nice -10"
    if [ "$kind" = "source" ]; then
        base="rubinius-$version"
        if [ ! -e "$base.tar.bz2" ]; then
            local down
            down=`_downloader "-LRO" ""`          || return 1
            _cmd "$down $siteurl/$base.tar.bz2"   || return 1
        fi
        _cmd "rm -rf rubinius-$version"           || return 1
        _cmd "$nice tar xjf $base.tar.bz2"        || return 1
        _cmd "cd rubinius-$version/"              || return 1
        _cmd "unset RUBYLIB"                      || return 1
        _cmd "export GEM_HOME=\$PWD/_gem"         || return 1
        _cmd "gem install bundler"                || return 1
        #_cmd "export PATH=\$PWD/_gem/bin:$PATH"   || return 1
        _cmd "_gem/bin/bundler"                   || return 1
        _cmd "time $nice $configure"              || return 1
        _cmd "time $nice _gem/bin/rake"           || return 1
        _cmd "cd .."                              || return 1
    fi
    ## verify
    local command="rbx"
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which $command"                         || return 1
    if [ "$prefix/bin/$command" != `which $command` ]; then
        echo "$prompt failed: $command command seems not installed correctly." 1>&2
        echo "$prompt exit 1" 1>&2
        return 1
    fi
    ## finish
    echo
    echo "$prompt Installation finished successfully."
    echo "$prompt   language:  $lang"
    echo "$prompt   version:   $version"
    echo "$prompt   directory: $prefix"
}


if [ -n "$1" -a -n "$2" ]; then
    if [ "root" = `whoami` ]; then
        echo "$prompt not allowed to execute by root user!" 1>&2
        echo "$prompt exit 1" 1>&2
        exit 1
    fi
    _install_rubinius "$1" "$2"
fi
