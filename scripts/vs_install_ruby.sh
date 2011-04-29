#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

_cmd() {
    echo '$' $1
    eval $1
}

_install_ruby() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang='ruby'
    local prompt="**"
    ## donwload, compile and install
    local ver
    case $version in
    1.8*)  ver="1.8";;
    1.9*)  ver="1.9";;
    *)     echo "versionswitcher: internal error: version=$version" 2>&1;;
    esac
    _cmd "wget -N ftp://ftp.ruby-lang.org/pub/ruby/$ver/ruby-$version.tar.bz2"
    _cmd "rm -rf ruby-$version"
    _cmd "tar xjf ruby-$version.tar.bz2"
    _cmd "cd ruby-$version/"
    _cmd "time ./configure --prefix=$prefix"
    _cmd "time make"
    _cmd "time make install"
    _cmd "cd .."
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"
    _cmd "hash -r"
    _cmd "which ruby"
    if [ "$prefix/bin/ruby" != `which ruby` ]; then
        echo "$prompt failed: ruby command seems not installed correctly." 2>&1
        echo "$prompt exit 1" 2>&1
        return 1
    fi
    ## install or update RubyGems
    local input
    case "$version" in
    1.8*)
        echo
        echo -n "$prompt Install RubyGems? [Y/n]: "
        read input
        [ -z "$input" ] && input="y"
        case "$input" in
        y*|Y*)
            _cmd "wget -N http://production.cf.rubygems.org/rubygems/rubygems-1.7.2.tgz"
            _cmd "tar xjf rubygems-1.7.2.tgz"
            _cmd "cd rubygems-1.7.2/"
            _cmd "$prefix/bin/ruby setup.rb"
            _cmd "cd .."
            _cmd "$prefix/bin/gem --version"
            echo "$prompt RubyGems installed successfully."
            ;;
        *)
            echo "$prompt skip to install RubyGems"
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
            _cmd "$prefix/bin/gem update --system"
            _cmd "$prefix/bin/gem --version"
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
        echo "$prompt not allowed to execute by root user!" 2>&1
        echo "$prompt exit 1" 2>&1
        exit 1
    fi
    _install_ruby "$1" "$2"
fi
