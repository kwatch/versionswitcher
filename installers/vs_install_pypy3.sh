#!/bin/sh

###
### $Release: 0.0.0 $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_pypy3() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="pypy3"
    local prompt="**"
    ## donwload, extract, and install
    local perl
    if   [ -f /usr/local/bin/perl ]; then perl="/usr/local/bin/perl"
    elif [ -f /usr/bin/perl ];       then perl="/usr/bin/perl"
    else                                  perl="perl"
    fi
    local url="https://bitbucket.org/pypy/pypy/downloads/"
    local rexp='href="/pypy/pypy/downloads/(pypy3[.\d]*-v?([.\d]+)-\w+[-\w]*)\.tar\.bz2"';
    down=`_downloader "-sL" "-q -O -"` || return 1
    local items=`eval $down $url | $perl -e '
        my $ver="'$version'";
        while (<>) {
            while (m!'$rexp'!g) {
                print $1, "\n" if $2 eq $ver;
            }
        }
    '`
    echo "$prompt Which one to install?"
    echo "$prompt"
    local i=0;
    for x in $items; do
        i=`expr $i + 1`
        echo "**    $i: $x";
    done
    echo "$prompt"
    echo -n "$prompt Select [1-$i]: "
    read input
    local base
    local j=0
    for x in $items; do
        j=`expr $j + 1`
        if [ $j = "$input" ]; then
            base=$x
            break
        fi
    done
    if [ -z "$base" ]; then
        echo "$prompt ERROR: invalid selection." 1>&2
        return 1
    fi
    ## inform required libraries
    local src_p=''
    case $base in
        *-src)  src_p="Y";;
    esac
    if [ -n "$src_p" ]; then
        _vs_inform_required_libraries "$prompt"   || return 1
    fi
    #
    local dlurl="https://bitbucket.org/pypy/pypy/downloads/$base.tar.bz2"
    if [ ! -e "$base.tar.bz2" ]; then
        local down
        #down=`_downloader "-LRO" "--no-check-certificate"` || return 1
        down=`_downloader "-LRO" ""`              || return 1
        _cmd "$down $dlurl"                       || return 1
    fi
    _cmd "rm -rf $base"                           || return 1
    _cmd "tar xjf $base.tar.bz2"                  || return 1
    local dirname=`tar tjf $base.tar.bz2 | awk -F/ 'NR==1 { print $1 }'`
    if [ -z "$dirname" ]; then
        echo "$prompt ERROR: failed to detect archive directory name." 1>&2
        echo "$prompt exit 1" 1>&2
        return 1
    fi
    #
    local opt=""
    local basedir=""
    if [ -n "$src_p" ]; then
        opt="-Ojit"                # get the JIT version
        #opt="-O2"                  # get the no-jit version
        #opt="-O2 --sandbox"        # get the sandbox version
        #opt="-O2 --stackless"      # get the stackless version
        #opt="-Ojit --backend=cli"  # only for branch/cli-jit
        _cmd "cd $dirname/pypy/translator/goal"   || return 1
        _cmd "time pypy3 translate.py $opt"       || return 1
        _cmd "cd ../../../.."                     || return 1
    else
        basedir=`dirname $prefix`
        _cmd "rm -rf $prefix"                     || return 1
        _cmd "mkdir -p $basedir"                  || return 1
        _cmd "mv $dirname $prefix"                || return 1
    fi
    ## create a link of 'bin/pypy3' as 'bin/python3'
    local input=""
    echo -n "$prompt Create a link of 'bin/pypy3' as 'bin/python3'? [Y/n]: "
    read input;  [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)  _cmd "(cd $prefix/bin/; ln -s pypy3 python; n -s pypy3 python3)" ;;
    esac
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which pypy3"                            || return 1
    if [ "$prefix/bin/pypy3" != `which pypy3` ]; then
        echo "$prefix ERROR: pypy3 command seems not installed correctly." 1>&2
        echo "$prefix exit 1" 1>&2
        return 1
    fi
    ## install 'pip'
    if [ ! -e "$prefix/bin/pip" ]; then
        echo
        echo -n "$prompt Install 'pip' command? [Y/n]: "
        read input;  [ -z "$input" ] && input="y"
        case "$input" in
        y*|Y*)
            local dlurl="https://bootstrap.pypa.io/get-pip.py"
            local down
            down=`_downloader "-ORL" "-N"`            || return 1
            _cmd "$down $dlurl"                       || return 1
            _cmd "$prefix/bin/pypy3 get-pip.py"        || return 1
            if [ ! -e "$prefix/bin/pip" ]; then
                echo "$prompt ERROR: failed to install 'pip' command." 1>&2
                echo "$prompt exit 1" 1>&2
                return 1
            fi
            echo "$prompt 'pip' command installed successfully."
            ;;
        *)
            echo "$prompt skip to install 'pip' command."
            ;;
        esac
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
    _install_pypy3 "$1" "$2"
fi
