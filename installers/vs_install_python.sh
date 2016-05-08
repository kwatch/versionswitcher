#!/bin/sh

###
### $Release: 0.0.0 $
### $License: Public Domain $
###

. $HOME/.vs/installers/vs_install.sh


_install_python() {
    ## arguments and variables
    local version=$1
    local prefix=$2
    local lang="python"
    local prompt="**"
    local flags=""
    ## platform-specific settings
    local macports_patch_url=""
    local readline_required=""
    local pythonver=""
    local platform=`uname`
    local input
    case "$platform" in
    Darwin*|darwin*)
        ## require macports patch?
        case "$version" in
        2.4*)  pythonver="python24";;
        2.5*)  pythonver="python25";;
        esac
        if [ -n "$pythonver" ]; then
            macports_patch_url="http://svn.macosforge.org/repository/macports/trunk/dports/lang/$pythonver"
            local svnpath=`which svn`
            if [ -z "$svnpath" ]; then
                echo "$prompt ERROR: you must install Subversion to apply MacPorts patch for Python $pythonver. Try 'sudo port install subversion' at first." 1>&2
                return 1
            fi
        fi
        ## require libreadline?
        if [ -n "$pythonver" ]; then
            if [ -f "/opt/local/lib/libreadline.dylib" ]; then
                flags="CPPFLAGS=-I/opt/local/include LDFLAGS=-L/opt/local/lib "
            elif [ -f "/usr/local/lib/libreadline.dylib" ]; then
                flags=""
            else
                echo "$prompt On Mac OS X, it is recommended to install readline library'"
                echo "$prompt by 'sudo port install readline'. Stop install? [Y/n]: "
                read input;  [ -z "$input" ] && input="y"
                case $input in
                y*|Y*)
                    echo "$prompt Installation process is stopped."
                    return 1
                    ;;
                esac
                flags=""
            fi
        else
            readline_required="YES"
        fi
        ;;
    esac
    ## for macports
    if [ -d '/opt/local/lib' ] && [ -d '/opt/local/include' ]; then
        echo -n "$prompt Use MacPorts files (/opt/local/*). OK? [Y/n]: "
        read input;  [ -z "$input" ] && input="y"
        case "$input" in
        y*|Y*)
            #flags="CFLAGS='-I/opt/local/include' LDFLAGS='-L/opt/local/lib' "
            flags="CFLAGS='-I/opt/local/include' CPPFLAGS='-I/opt/local/include' LDFLAGS='-L/opt/local/lib' "
            ;;
        esac
    fi
    ## confirm configure option
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
    ## inform required libraries
    _vs_inform_required_libraries "$prompt"       || return 1
    ## donwload and compile
    local ver=$version
    case $version in
    2.*|3.0*|3.1*|3.2*)
        ver=`echo $version | sed 's/\.0$//'` ;;
    esac
    local base="Python-$ver"
    local filename="$base.tgz"
    local url="http://www.python.org/ftp/python/$ver/$filename"
    local nice="nice -10"
    if [ ! -e "$filename" ]; then
        local down
        down=`_downloader "-LRO" ""`              || return 1
        _cmd "$down $url"                         || return 1
    fi
    _cmd "rm -rf $base"                           || return 1
    _cmd "$nice tar xzf $filename"                || return 1
    _cmd "cd $base/"                              || return 1
    if [ -n "$macports_patch_url" ]; then
        _cmd "svn checkout $macports_patch_url"   || return 1
        for i in $pythonver/files/patch-*.diff; do
            _cmd "patch -p0 < $i"                 #|| return 1
        done
    fi
    _cmd "${flags}time $nice $configure"          || return 1
    _cmd "time $nice make"                        || return 1
    ## ad-hoc patch to compile 'pyexpat' module
    if ./python.exe -c "import pyexpat" 2>/dev/null; then
        :   # do nothing
    else
        echo "$prompt Apply ad-hoc patch to compile 'pyexpat' module"
        cat <<EOF > tmp.patch
Ad-hoc patch to compile 'pyexpat' module.

original: https://github.com/LibreOffice/core/blob/master/external/python3/python-3.3.5-pyexpat-symbols.patch.1

--- python3/Modules/expat/expat_external.h
+++ python3/Modules/expat/expat_external.h
@@ -7,10 +7,6 @@

 /* External API definitions */

-/* Namespace external symbols to allow multiple libexpat version to
-   co-exist. */
-#include "pyexpatns.h"
-
 #if defined(_MSC_EXTENSIONS) && !defined(__BEOS__) && !defined(__CYGWIN__)
 #define XML_USE_MSC_EXTENSIONS 1
 #endif
EOF
        patch -p1 < tmp.patch                     || return 1
        _cmd "time $nice make"                    || return 1
    fi
    ## install
    local make_target
    case $version in
    3.0*)  make_target="fullinstall";;
    *)     make_target="install";;
    esac
    _cmd "time $nice make $make_target"           || return 1
    _cmd "cd .."                                  || return 1
    ## create a link of 'bin/python3' as 'bin/python'
    if [ ! -f "$prefix/bin/python" ]; then
        local ver=`echo $version | sed 's/^\([0-9]\.[0-9]\).*/\1/'`
        _cmd "(cd $prefix/bin/; ln python$ver python)"
    fi
    ## verify
    _cmd "export PATH=$prefix/bin:$PATH"          || return 1
    _cmd "hash -r"                                || return 1
    _cmd "which python"                           || return 1
    if [ "$prefix/bin/python" != `which python` ]; then
        echo "$prefix ERROR: python command seems not installed correctly." 1>&2
        echo "$prefix exit 1" 1>&2
        return 1
    fi
    ## install 'easy_install'
    local easy_install_path
    local script='distribute_setup.py'
    echo
    echo -n "$prompt Install 'easy_install' command? [y/N]: "
    read input;  [ -z "$input" ] && input="n"
    case "$input" in
    y*|Y*)
        #url="http://python-distribute.org/$script"
        url="http://bit.ly/distribute_setup_py"
        local down
        down=`_downloader "-RLo $script" "-NO $script"` || return 1
        _cmd "$down $url"                         || return 1
        _cmd "$prefix/bin/python $script"         || return 1
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
    ## install 'readline' package (for Mac OS X)
    if [ -n "$readline_required" -a -n "$easy_install_path" ]; then
        echo
        echo -n "$prompt Install 'readline' package? (recommended for Mac OS X) [Y/n]: "
        read input;  [ -z "$input"] && input="y"
        case "$input" in
        y*|Y*)
            _cmd "easy_install readline"          || return 1
            ;;
        *)
            echo "$prompt skip to install readline package."
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
    _install_python "$1" "$2"
fi
