#!/bin/sh

###
### $Release: 0.0.0 $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_rust() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="rust"
    local prompt="**"
    local archives_url='https://www.rust-lang.org/downloads.html'
    local installer_url='https://static.rust-lang.org/rustup.sh'
    local nice="nice -10"
    ## download installer
    _cmd "rm -f rustup.sh"
    local down
    down=`_downloader "-LRO" ""`              || return 1
    _cmd "$down $installer_url"               || return 1
    ## run instalelr script
    local opt
    case $version in
      beta)     opt='--channel=beta'      ;;
      nightly)  opt='--channel=nightly'   ;;
      *)        opt="--revision=$version" ;;
    esac
    _cmd "sh rustup.sh --prefix=$prefix $opt --yes"     || return 1
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"                || return 1
    _cmd "hash -r"                                      || return 1
    _cmd "which rustc"                                  || return 1
    if [ "$prefix/bin/rustc" != `which rustc` ]; then
        echo "$prefix ERROR: rustc command seems not installed correctly." 1>&2
        echo "$prefix exit 1" 1>&2
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
        echo "*** not allowed to execute by root user!" 1>&2
        echo "*** exit 1" 1>&2
        exit 1
    fi
    _install_rust "$1" "$2"
fi
