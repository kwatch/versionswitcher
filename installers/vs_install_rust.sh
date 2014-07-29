#!/bin/sh

###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011-2012 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_rust() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="rust"
    local prompt="**"
    local archives_url='http://www.rust-lang.org/install.html'
    local download_url='http://static.rust-lang.org/dist'
    local nice="nice -10"
    ##
    perl='perl';
    [ -f /usr/local/bin/perl ] && perl='/usr/local/bin/perl';
    [ -f /usr/bin/perl ]       && perl='/usr/bin/perl';
    ## donwload, extract, and install
    local ver=$version
    local down
    down=`_downloader "-sL" "-q -O - --no-check-certificate"` || return 1
    $down $archives_url | $perl -e '
    my $i = 0;
    while (<>) {
      if (/\/dist\/(rust-'$ver'.*?\.tar\.gz)"/) {
        print "\n** Which one to install?\n" if $i == 0;
        print ++$i, ": ", $1, "\n";
      }
    }
    if ($i) {
      print "\n";
      print "** Select [1-$i]: ";
    } else {
      print "** Download file not found. Exit.\n";
      exit 1
    }
    '
    if [ $? -ne 0 ]; then
        return 1
    fi
    local num
    read num
    base=`$down $archives_url | $perl -e '
    my $i = 0;
    while (<>) {
      if (/\/dist\/(rust-'$ver'.*?)\.tar\.gz"/) {
        if (++$i eq '$num') {
          print $1;
          break;
        }
      }
    }
    '`
    if [ -z "$base" ]; then
        echo "$prompt Not install. Exit."
        return 0
    fi
    local fname="$base.tar.gz"
    if [ ! -e "$fname" ]; then
        down=`_downloader "-LRO" "--no-check-certificate"`    || return 1
        _cmd "$down $download_url/$fname"               || return 1
    fi
    local basedir=`dirname $prefix`
    _cmd "mkdir -p $basedir"                            || return 1
    _cmd "rm -rf $prefix"                               || return 1
    _cmd "rm -rf $basedir/$base"                        || return 1
    case "$fname" in
    rust-*-*.tar.gz)
        _cmd "$nice tar -C $basedir -xzf $fname"        || return 1
        _cmd "mv $basedir/$base $prefix"                || return 1
        ;;
    *)
        _cmd "$nice tar -xzf $fname"                    || return 1
        _cmd "cd $base"                                 || return 1
        _cmd "time $nice ./configure --prefix=$prefix"  || return 1
        _cmd "time $nice make"                          || return 1
        _cmd "time $nice make install"                  || return 1
        ;;
    esac
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
