#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011-2012 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_ruby() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang='ruby'
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
    ## *.tar.bz2 is provided since 1.8.5-p52
    local ext='tar.bz2'
    local tar='tar xjf'
    case $version in
    1.8.[0-5]*)
        ext='tar.gz'
        tar='tar xzf'
        ;;
    esac
    ## donwload, compile and install
    local ver
    case $version in
    1.8*)  ver="1.8";;
    1.9*)  ver="1.9";;
    *)
        echo "$prompt ERROR: version $version is not supported to install." 1>&2
        return 1
        ;;
    esac
    local base="ruby-$version"
    local filename="$base.$ext"
    local url="ftp://ftp.ruby-lang.org/pub/ruby/$ver/$filename"
    local nice="nice -10"
    if [ ! -f "$filename" ]; then
        local down=`_downloader "-ORL" "-N"`      || return 1
        _cmd "$down $url"                         || return 1
    fi
    _cmd "rm -rf $base"                           || return 1
    _cmd "$nice $tar $base.$ext"                  || return 1
    _cmd "cd $base/"                              || return 1
    _cmd "time $nice $configure"                  || return 1
    _cmd "time $nice make"                        || return 1
    _cmd "time $nice make install"                || return 1
    _cmd "cd .."                                  || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which ruby"                             || return 1
    if [ "$prefix/bin/ruby" != `which ruby` ]; then
        echo "$prompt failed: ruby command seems not installed correctly." 1>&2
        echo "$prompt exit 1" 1>&2
        return 1
    fi
    ## install or update RubyGems
    case "$version" in
    1.8*)
        echo
        echo -n "$prompt Install RubyGems? [Y/n]: "
        read input
        [ -z "$input" ] && input="y"
        case "$input" in
        y*|Y*)
            base="rubygems-1.8.11"
            url="http://production.cf.rubygems.org/rubygems/$base.tgz"
            local down=`_downloader "-ORL" "-N"`             || return 1
            _cmd "$down $url"                                || return 1
            _cmd "tar xzf $base.tgz"                         || return 1
            _cmd "cd $base/"                                 || return 1
            _cmd "$prefix/bin/ruby setup.rb"                 || return 1
            _cmd "cd .."                                     || return 1
            _cmd "$prefix/bin/gem update --system"           || return 1
            _cmd "$prefix/bin/gem --version"                 || return 1
            echo "$prompt RubyGems installed successfully."
            ;;
        *)
            echo "$prompt Skip to install RubyGems"
            ;;
        esac
        ;;
    1.9*)
        echo
        echo -n "$prompt Update RubyGems? [Y/n]: "
        read input
        [ -z "$input" ] && input="y"
        case "$input" in
        y*|Y*)
            _cmd "$prefix/bin/gem update --system"          || return 1
            _cmd "$prefix/bin/gem --version"                || return 1
            echo "$prompt RubyGems updated successfully."
            ;;
        *)
            echo "$prompt skip to update RubyGems"
            ;;
        esac
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
        echo "$prompt not allowed to execute by root user!" 1>&2
        echo "$prompt exit 1" 1>&2
        exit 1
    fi
    _install_ruby "$1" "$2"
fi
