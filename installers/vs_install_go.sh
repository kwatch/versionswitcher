#!/bin/sh

###
### $Release: 0.0.0 $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_go() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="go"
    local prompt="**"
    local archives_url='http://golang.org/dl/'
    local download_url='http://golang.org/dl'
    ##
    local perl='perl';
    [ -f /usr/local/bin/perl ] && perl='/usr/local/bin/perl';
    [ -f /usr/bin/perl ]       && perl='/usr/bin/perl';
    ## donwload, extract, and install
    local ver=`echo $version | sed 's/\.0$//'`
    local verpat=`echo $ver | sed 's/\./\\\\./g'`
    local down
    down=`_downloader "-sL" "-q -O -"` || return 1
    local items=`$down $archives_url | $perl -e '
    my %checked;
    while (<>) {
      while (/href="https:\/\/dl\.google\.com\/go\/(go'$verpat'\.[^.]+)\.tar\.gz">go/g) {
        last if exists($checked{$1});
        $checked{$1} = 1;
        print $1, "\n";
      }
    }'`
    if [ -z "$items" ]; then
        echo "$prompt Download file not found. Exit." 1>&2;
        exit 1
    fi
    #
    echo ""
    echo "$prompt Which one to install?"
    local i=0;
    for x in $items; do
        i=`expr $i + 1`
        echo "$i: $x"
    done
    echo ""
    echo -n "$prompt Select [1-$i]: ";
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
        echo "$prompt Not install. exit."
        return 0
    fi
    local fname="$base.tar.gz"
    if [ ! -e "$fname" ]; then
        down=`_downloader "-LRO" "--no-check-certificate"` || return 1
        _cmd "$down $download_url/$fname"         || return 1
    fi
    local prefix_basedir=`dirname $prefix`
    _cmd "mkdir -p $prefix"                       || return 1
    _cmd "rm -rf $prefix"                         || return 1
    _cmd "rm -rf $prefix_basedir/go"              || return 1
    _cmd "tar -C $prefix_basedir -xzf $fname"     || return 1
    _cmd "mv $prefix_basedir/go $prefix"          || return 1
    case "$base" in
    *.src)
        ## inform required libraries
        _vs_inform_required_libraries "$prompt"   || return 1
        ##
        _cmd "(cd $prefix/src; ./all.bash)"       || return 1
        ;;
    esac
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which go"                               || return 1
    if [ "$prefix/bin/go" != `which go` ]; then
        echo "$prefix ERROR: go command seems not installed correctly." 1>&2
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
    _install_go "$1" "$2"
fi
