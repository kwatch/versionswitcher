###
### $Release: 0.0.0 $
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
__vs_help_message() {
        cat <<END
versionswitcher - change version of language or application
release: $release
examples:
    $ VERSIONSWITCHER_PATH=\$HOME/lang
    $ vs -h               # show help
    $ vs                  # list language names installed
    $ vs python           # list python vesrions installed
    $ vs python 2.6.6     # use \$HOME/lang/python/2.6.6
    $ vs python 2         # use \$HOME/lang/python/2.x.x (ex. 2.7.1)
    $ vs python latest    # use latest version under \$HOME/lang/python
    $ vs python -         # use system-installed one (ex. /usr/bin/python)
    $ vs -i               # list language names installable
    $ vs -i python        # list python versions installable
    $ vs -i python latest # install python latest version (ex. 3.2.0)

tips:
    * Short name 'vs' is an alias to 'versionswitcher'.
    * It is allowed to set VERSIONSWITCHER_PATH=path1:path2:path3:...
    * \$HOME/.versionswitcher/hooks/<language>.sh is imported if exists.
END
}


###
versionswitcher() {
    local lang
    local version
    local release=`echo '$Release: 0.1.0 $' | awk '{print $2}'`
    __vs_option_quiet=''
    case "$1" in
    -q)
        __vs_option_quiet='true'
        shift;;
    esac
    case "$1" in
    -h|--help)
        __vs_help_message
        ;;
    -v|--version)
        echo $release
        ;;
    -i|--install)
        lang=$2; version=$3
        __vs_install "$lang" "$version"
        ;;
    -*)
        echo "versionswitcher: $1: unknown option." 2>&1
        ;;
    *)
        lang=$1
        version=$2
        case $lang in
        ruby|rb)       __vs_switch ruby      ruby     "$version";;
        python|py)     __vs_switch python    python   "$version";;
        perl)          __vs_switch perl      perl     "$version";;
        rubinius|rbx)  __vs_switch rubinius  rbx      "$version";;
        gauche|gosh)   __vs_switch gauche    gosh     "$version";;
        *)             __vs_switch $lang     $lang    "$version";;
        esac
        ;;
    esac
    unset __vs_option_quiet
}


###
__vs_glob() {
    local pattern=$1
    local filenames
    if [ -n "$BASH_VERSION" ]; then            # for bash
        (shopt -s nullglob; echo $pattern)
    elif [ -n "$ZSH_VERSION" ]; then           # for zsh
        (setopt nonomatch; setopt nullglob; eval echo $pattern)
    else                                       # other
        filenames=`echo $pattern`
        [ "$filenames" == "$pattern" ] || echo $filenames
    fi
}


###
__vs_echo() {
    if [ -z "$__vs_option_quiet" ]; then
        echo $1
    fi
}


###
__vs_versions() {
    local basedir=$1
    local version=$2
    __vs_glob "$basedir/$version*/bin" | awk '{
      for (i=1; i<=NF; i++) {
        binpath = $i;
        split(binpath, arr, "/");
        version = arr[length(arr)-1];
        split(version, nums, /[^0-9]+/);
        key = "";
        len = length(nums);
        for (j=1; j<=len; j++) {
          if (length(nums[j]) > 0) {
            key = key sprintf("%010d", nums[j]) "_";
          }
        }
        if (len == 0) { key = version }
        print key, version;
      }
    }' | sort | awk '{print $2}'
}


##
__vs_error() {
    local msg=$1
    echo "versionswitcher: $msg" 2>&1
    return 1
}


###
__vs_switch() {
    local lang=$1
    local command=$2
    local version=$3
    ## exit if $VERSIONSWITCHER_PATH is not set
    [ -n "$VERSIONSWITCHER_PATH" ] || __vs_error '$VERSIONSWITCHER_PATH is not set.' || return 1
    ## show all language names if lang is not specified
    local dir
    local basedir
    local list
    if [ -z "$lang" ]; then
        #echo "## language          # basedir"
        __vs_echo "## installed"
        for dir in `echo $VERSIONSWITCHER_PATH | tr ':' ' '`; do
            for basedir in `__vs_glob "$dir/*"`; do
                list=`__vs_glob "$basedir/*/bin"`
                if [ -n "$list" ]; then
                    lang=`basename $basedir`
                    printf "%-20s # %s\n" $lang $basedir
                fi
            done
        done | awk '{if(++D[$1]==1)print}' | sort
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
    [ -n "$basedir" ] || __vs_error "$lang is not installed." || return 1
    ## list available versions if version is not specified
    if [ -z "$version" ]; then
        __vs_echo "## basedir: $basedir"
        __vs_echo "## versions:"
        __vs_versions "$basedir"
        return 0
    fi
    ## find 'bin' directory
    local bindir
    local ver
    if [ "$version" = "-" ]; then
        bindir=""
    elif [ "$version" = "latest" ]; then
        ver=`__vs_versions "$basedir" | tail -1`
        bindir=""
        [ -n "$ver" ] && bindir="$basedir/$ver/bin"
    else
        bindir="$basedir/$version/bin"
        if ! [ -d "$bindir" ]; then
            ver=`__vs_versions "$basedir" "$version" | tail -1`
            bindir=""
            [ -n "$ver" ] && bindir="$basedir/$ver/bin"
        fi
    fi
    [ -n "$bindir" -o "$version" = "-" ] || __vs_error "$lang version $version is not installed." || return 1
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
    __vs_echo "$prompt export PATH=$newpath"    ; export PATH=$newpath
    hash -r
    ## set or clear ${lang}root
    local rootvar="${lang}root"
    #local vervar=`awk 'BEGIN{print toupper("VERSIONSWITCHER_'$lang'_VERSION")}'`
    local vervar="${lang}version"
    if [ -n "$bindir" ]; then
        rootdir=`dirname $bindir`
        version=`basename $rootdir`
        __vs_echo "$prompt $rootvar='$rootdir'" ; eval "$rootvar=$rootdir"
        __vs_echo "$prompt $vervar='$version'"  ; eval "$vervar='$version'"
    else
        __vs_echo "$prompt unset $rootvar"      ; unset $rootvar
        __vs_echo "$prompt unset $vervar"       ; unset $vervar
    fi
    ## show command path
    echo "$prompt which $command"          ; which $command
    ## import hook script if exists
    local script="$HOME/.versionswitcher/hooks/$lang.sh"
    [ -f "$script" ] && . $script
}


###
__vs_download() {
    local filename=$1
    local url="http://versionswitcher.appspot.com/$filename"
    if [ -n "$VS_DEBUG" ]; then
        url="http://localhost:8080/$filename"
    fi
    local vs_home="$HOME/.versionswitcher"
    local dir=`dirname $filename`
    [ "$dir" = "." ] && dir=""
    if [ -n "$dir" -a ! -d "$vs_home/$dir" ]; then
        mkdir -p $vs_home/$dir || __vs_error "Failed: mkdir -p $vs_home/$dir" || return 1
    fi
    (cd $vs_home/$dir; wget -Nq $url) || __vs_error "Failed: wget -Nq $url" || return 1
    echo $vs_home/$filename
}


###
__vs_install() {
    local lang=$1
    local version=$2
    local filepath
    local prompt='**'
    ## list all languages when lang is not specified
    if [ -z "$lang" ]; then
        filepath=`__vs_download versions/INDEX.txt`
        [ -f "$filepath" ] || __vs_error "INDEX.txt: not found." || return 1
        __vs_echo "## try 'vs -i LANG' where LANG is one of:"
        cat $filepath
        return 0
    fi
    ## find version file
    filepath=`__vs_download versions/${lang}.txt`
    [ -f "$filepath" ] || __vs_error "$lang is not supported to install." || return 1
    ## show all versions when version is not specified
    if [ -z "$version" ]; then
        __vs_echo "## try 'vs -i $lang VERSION' where VERSION is one of:"
        cat $filepath
        return 0
    fi
    ## detect latest version when 'latest' is specified
    local input
    local found=""
    local ver
    if [ "$version" = "latest" ]; then
        version=`awk 'NR==1{print $1}' "$filepath"`
        [ -n "$version" ] || __vs_error "failed to detect latest version." || return 1
        __vs_echo "$prompt latest version is $version"
    ## verify version
    else
        for ver in `cat $filepath`; do
            [ "$ver" = "$version" ] && found=true
        done
        if [ -z "$found" ]; then
            echo -n "$prompt Are you really to install $lang $version? [y/N]: "
            read input
            [ -z "$input" ] && input="n"
            case $input in
            y*|Y*)  ;;
            *)      return 1;;
            esac
        fi
    fi
    ## find installer script file
    local script_file=`__vs_download scripts/vs_install_${lang}.sh`
    [ -f "$script_file" ] || __vs_error "$lang is not supported to install." || return 1
    ## confirm PREFIX directory
    [ -n "$VERSIONSWITCHER_PATH" ] || __vs_error "Set \$VERSIONSWITCHER_PATH before installation." || return 1
    local inst_dir=`echo $VERSIONSWITCHER_PATH | awk -F: '{print $1}'`
    local prefix="$inst_dir/$lang/$version"
    echo -n "$prompt Install into '$prefix'. OK? [Y/n]: "
    read input
    [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)
        ;;
    *)
        echo -n "$prompt Enter direcotry (full path): "
        read prefix
        [ -n "$prefix" ] || __vs_error "Install path is not entered." || return 1
        ;;
    esac
    ## invoke installer script
    local shell=$SHELL
    [ -z "$shell" ] && shell="/bin/sh"
    $shell "$script_file" "$version" "$prefix" || __vs_error "Failed to install." || return 1
    ## switch to it
    echo
    echo "$prompt vs $lang $version"  ; versionswitcher $lang $version
}


###
#alias vs=versionswitcher
vs() {
    versionswitcher $@
}
