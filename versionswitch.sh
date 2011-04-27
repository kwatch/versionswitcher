##
## versionswitch.sh -- switch version of language or application
##
## setup:
##   $ VERSIONSWITCH_PATH=$HOME/lang
##   $ . /some/where/to/versionswitch.sh'
##   $ vs --help
##


##
#[ -z "$VERSIONSWITCH_PATH" ] && VERSIONSWITCH_PATH=$HOME/local/lang


##
versionswitch () {
    local lang=$1
    local version=$2
    local release=`echo '$Release: 0.1.0 $' | awk '{print $2}'`
    case $lang in
    -h|--help)
        cat <<END
versionswitch - change version of language or application
release: $release
examples:
    $ VERSIONSWITCH_PATH=\$HOME/lang
    $ vs -h             # show help
    $ vs foobar 1.2.3   # use \$HOME/lang/foobar/1.2.3
    $ vs foobar 1.2     # use \$HOME/lang/foobar/1.2.x (ex. 1.2.8)
    $ vs foobar latest  # use latest version under \$HOME/lang/foobar
    $ vs foobar -       # use system-installed one (ex. /usr/bin/foobar)
    $ vs foobar         # show installed versions of foobar
    $ vs                # show installed languages

tips:
    * Short name 'vs' is an alias to 'versionswitch'.
    * It is allowed to set VERSIONSWITCH_PATH=path1:path2:path3:...
    * \$HOME/.versionswitch/hooks/<language>.sh is imported if exists.
END
        ;;
    -v|--version)
        echo $release
        ;;
    ruby|rb)       _versionswitch ruby      ruby     "$version";;
    python|py)     _versionswitch python    python   "$version";;
    perl)          _versionswitch perl      perl     "$version";;
    rubinius|rbx)  _versionswitch rubinius  rbx      "$version";;
    gauche|gosh)   _versionswitch gauche    gosh     "$version";;
    *)             _versionswitch $lang     $lang    "$version";;
    esac
}


##
__vs_glob() {
    local pattern=$1
    local filenames
    if [ -n "$BASH_VERSIONK" ]; then           # for bash
        (shopt -s nullglob; echo $pattern)
    elif [ -n "$ZSH_VERSION" ]; then           # for zsh
        (setopt nonomatch; setopt nullglob; eval echo $pattern)
    else                                       # other
        filenames=`echo $pattern`
        [ "$filenames" == "$pattern" ] || echo $filenames
    fi
}

##
_versionswitch () {
    local lang=$1
    local command=$2
    local version=$3
    ## exit if $VERSIONSWITCH_PATH is not set
    if [ -z "$VERSIONSWITCH_PATH" ]; then
        echo 'versionswitch: $VERSIONSWITCH_PATH is not set.' 2>&1
        return 1
    fi
    ## show all language names if lang is not specified
    local dir
    local basedir
    local list
    if [ -z "$lang" ]; then
        #echo "## language          # basedir"
        echo "## installed"
        for dir in `echo $VERSIONSWITCH_PATH | tr ':' ' '`; do
            for basedir in `__vs_glob "$dir/*"`; do
                list=`__vs_glob "$basedir/*/bin"`
                if [ -n "$list" ]; then
                    lang=`basename $basedir`
                    printf "%-20s # %s\n" $lang $basedir
                fi
            done
        done | sort
        return 0
    fi
    ## check whether installed or not
    local basedir=''
    for dir in `echo $VERSIONSWITCH_PATH | tr ':' ' '`; do
        if [ -n "$dir" -a -d "$dir/$lang" ]; then
            basedir="$dir/$lang"
            break
        fi
    done
    if [ -z "$basedir" ]; then
        echo "versionswitch: $lang is not installed." 2>&1
        return 1
    fi
    ## list available versions if version is not specified
    local ver
    if [ -z "$version" ]; then
        echo "## basedir: $basedir"
        echo "## versions:"
        for dir in `__vs_glob "$basedir/*/bin"`; do
            basename `dirname $dir`
        done
        return 0
    fi
    ## find 'bin' directory
    local bindir
    if [ "$version" = "-" ]; then
        bindir=""
    elif [ "$version" = "latest" ]; then
        bindir=`__vs_glob "$basedir/*/bin"`
    else
        bindir="$basedir/$version/bin"
        if ! [ -d "$bindir" ]; then
            bindir=`__vs_glob "$basedir/$version*/bin" | awk '{print $NF}'`
        fi
    fi
    if [ -z "$bindir" -a "$version" != "-" ]; then
        echo "versionswitch: $lang version $version is not installed." 2>&1
        return 1
    fi
    ## remove current bindir from $PATH
    #local newpath=`ruby -e "print ENV['PATH'].split(':').delete_if{|x|x=~%r'^$basedir/.*/bin'}.join(':')"`
    local newpath=$bindir
    for dir in `echo $PATH | tr ':' ' '`; do
        case $dir in
        $basedir/*/bin*)
            ;;
        *)
            if [ -z "$newpath" ]; then
                newpath=$dir
            else
                newpath=$newpath:$dir
            fi
            ;;
        esac
    done
    ## set $PATH
    local prompt='$'  # or '[versionswitch]$'
    echo "$prompt export PATH=$newpath"     ; export PATH=$newpath
    hash -r
    ## set or clear ${lang}root
    local rootvar="${lang}root"
    #local vervar=`awk 'BEGIN{print toupper("VERSIONSWITCH_'$lang'_VERSION")}'`
    local vervar="${lang}version"
    if [ -n "$bindir" ]; then
        rootdir=`dirname $bindir`
        version=`basename $rootdir`
        echo "$prompt $rootvar='$rootdir'" ; eval "$rootvar=$rootdir"
        echo "$prompt $vervar='$version'"  ; eval "$vervar='$version'"
    else
        echo "$prompt unset $rootvar"      ; unset $rootvar
        echo "$prompt unset $vervar"       ; unset $vervar
    fi
    ## show command path
    echo "$prompt which $command"          ; which $command
    ## import hook script if exists
    local script="$HOME/.versionswitch/hooks/$lang.sh"
    [ -f "$script" ] && . $script
}


##
alias vs=versionswitch
