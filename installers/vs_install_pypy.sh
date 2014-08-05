#!/bin/sh

###
### $Release: 0.0.0 $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_pypy() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="pypy"
    local prompt="**"
    ## platform-specific settings
    case `uname` in
    Darwin*|darwin*)
        target="osx64";;
    Linux*|linux*)
        case `uname -m` in
        x86_64|amd64)  target="linux64";;
        i686|i386)     target="linux"  ;;
        *)             target="linux"  ;;
        esac
        ;;
    *)
        target="src";;
    esac
    ## inform required libraries
    if [ "$target" = "src" ]; then
        _vs_inform_required_libraries "$prompt"   || return 1
    fi
    ## donwload, extract, and install
    local ver=`echo $version | sed 's/\.0$//'`
    local base="pypy-$ver-$target"
    local url="https://bitbucket.org/pypy/pypy/downloads/$base.tar.bz2"
    if [ ! -e "$base.tar.bz2" ]; then
        local down
        down=`_downloader "-LRO" "--no-check-certificate"` || return 1
        _cmd "$down $url"                         || return 1
    fi
    _cmd "rm -rf $base"                           || return 1
    _cmd "tar xjf $base.tar.bz2"                  || return 1
    local dirname=`tar tjf $base.tar.bz2 | awk -F/ 'NR==1 { print $1 }'`
    if [ -z "$dirname" ]; then
        echo "$prompt ERROR: failed to detect archive directory name." 1>&2
        echo "$prompt exit 1" 1>&2
        return 1
    fi
    local opt=""
    local basedir=""
    if [ "$target" = "src" ]; then
        opt="-Ojit"                # get the JIT version
        #opt="-O2"                  # get the no-jit version
        #opt="-O2 --sandbox"        # get the sandbox version
        #opt="-O2 --stackless"      # get the stackless version
        #opt="-Ojit --backend=cli"  # only for branch/cli-jit
        _cmd "cd $dirname/pypy/translator/goal"   || return 1
        _cmd "time pypy translate.py $opt"        || return 1
        _cmd "cd ../../../.."                     || return 1
    else
        basedir=`dirname $prefix`
        _cmd "rm -rf $prefix"                     || return 1
        _cmd "mkdir -p $basedir"                  || return 1
        _cmd "mv $dirname $prefix"                || return 1
    fi
    ## create a link of 'bin/pypy' as 'bin/python'
    local input=""
    echo -n "$prompt Create a link of 'bin/pypy' as 'bin/python'? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)  _cmd "(cd $prefix/bin/; ln -s pypy python)" ;;
    esac
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which pypy"                             || return 1
    if [ "$prefix/bin/pypy" != `which pypy` ]; then
        echo "$prefix ERROR: pypy command seems not installed correctly." 1>&2
        echo "$prefix exit 1" 1>&2
        return 1
    fi
    ## install 'easy_install'
    local easy_install_path
    local script='distribute_setup.py'
    echo
    echo -n "$prompt Install 'easy_install' command? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)
        url="http://python-distribute.org/$script"
        local down
        down=`_downloader "-ORL" "-N"`            || return 1
        _cmd "$down $url"                         || return 1
        _cmd "$prefix/bin/pypy $script"           || return 1
        _cmd "which easy_install"                 || return 1
        easy_install_path=`which easy_install`
        if [ "$easy_install_path" != "$prefix/bin/easy_install" ]; then
            echo "$prompt ERROR: easy_install command seems not installed correctly." 1>&2
            echo "$prompt exit 1" 1>&2
            return 1
        fi
        echo "$prompt easy_install command installed successfully."
        ;;
    *)
        echo "$prompt skip to install easy_install command."
        ;;
    esac
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
    _install_pypy "$1" "$2"
fi
