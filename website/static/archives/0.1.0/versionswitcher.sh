###
### $Release: 0.1.0 $
### $Copyright: copyright(c) 2011 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

###
### versionswitcher.sh -- switch version of language or application
###
### setup:
###   $ VERSIONSWITCHER_PATH=$HOME/lang
###   $ . /some/where/to/versionswitcher.sh'
###   $ vs --help
###


###
[ -z "$VERSIONSWITCHER_PATH" -a -d $HOME/lang ] && VERSIONSWITCHER_PATH=$HOME/lang


###
versionswitcher() {
    local lang=$1
    local version=$2
    local release=`echo '$Release: 0.1.0 $' | awk '{print $2}'`
    case $lang in
    -h|--help)
        cat <<END
versionswitcher - change version of language or application
release: $release
examples:
    $ VERSIONSWITCHER_PATH=\$HOME/lang
    $ vs -h             # show help
    $ vs python 2.6.6   # use \$HOME/lang/python/2.6.6
    $ vs python 2       # use \$HOME/lang/python/2.x.x (ex. 2.7.1)
    $ vs python latest  # use latest version under \$HOME/lang/python
    $ vs python -       # use system-installed one (ex. /usr/bin/python)
    $ vs python         # show installed versions of python
    $ vs                # show installed languages

tips:
    * Short name 'vs' is an alias to 'versionswitcher'.
    * It is allowed to set VERSIONSWITCHER_PATH=path1:path2:path3:...
    * \$HOME/.versionswitcher/hooks/<language>.sh is imported if exists.
END
        ;;
    -v|--version)
        echo $release
        ;;
    ruby|rb)       __vs_switch ruby      ruby     "$version";;
    python|py)     __vs_switch python    python   "$version";;
    perl)          __vs_switch perl      perl     "$version";;
    rubinius|rbx)  __vs_switch rubinius  rbx      "$version";;
    gauche|gosh)   __vs_switch gauche    gosh     "$version";;
    *)             __vs_switch $lang     $lang    "$version";;
    esac
}


###
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

###
__vs_switch() {
    local lang=$1
    local command=$2
    local version=$3
    ## exit if $VERSIONSWITCHER_PATH is not set
    if [ -z "$VERSIONSWITCHER_PATH" ]; then
        echo 'versionswitcher: $VERSIONSWITCHER_PATH is not set.' 2>&1
        return 1
    fi
    ## show all language names if lang is not specified
    local dir
    local basedir
    local list
    if [ -z "$lang" ]; then
        #echo "## language          # basedir"
        echo "## installed"
        for dir in `echo $VERSIONSWITCHER_PATH | tr ':' ' '`; do
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
    for dir in `echo $VERSIONSWITCHER_PATH | tr ':' ' '`; do
        if [ -n "$dir" -a -d "$dir/$lang" ]; then
            basedir="$dir/$lang"
            break
        fi
    done
    if [ -z "$basedir" ]; then
        echo "versionswitcher: $lang is not installed." 2>&1
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
        echo "versionswitcher: $lang version $version is not installed." 2>&1
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
    local prompt='$'  # or '[versionswitcher]$'
    echo "$prompt export PATH=$newpath"     ; export PATH=$newpath
    hash -r
    ## set or clear ${lang}root
    local rootvar="${lang}root"
    #local vervar=`awk 'BEGIN{print toupper("VERSIONSWITCHER_'$lang'_VERSION")}'`
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
    local script="$HOME/.versionswitcher/hooks/$lang.sh"
    [ -f "$script" ] && . $script
}


###
alias vs=versionswitcher
