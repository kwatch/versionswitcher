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
_versionswitch () {
    local lang=$1
    local command=$2
    local version=$3
    ## exit if $VERSIONSWITCH_PATH is not set
    if [ -z "$VERSIONSWITCH_PATH" ]; then
        echo 'versionswitch: $VERSIONSWITCH_PATH is not set.'
        return 1
    fi
    ## show all language names if lang is not specified
    local dir
    local basedir
    local list
    if [ -z "$lang" ]; then
        #echo "## language          # basedir"
        echo "## installed"
        for dir in `echo $VERSIONSWITCH_PATH | awk -F: '{for(i=1;i<=NF;i++){print $i}}'`; do
            for basedir in `echo $dir/*`; do
                #if [ "$basedir" != "$dir/*" ]; then
                    list=`echo $basedir/*/bin`
                    if [ "$list" != "$basedir/*/bin" ]; then
                        lang=`basename $basedir`
                        printf "%-20s # %s\n" $lang $basedir
                    fi
                #fi
            done
        done | sort
        return 0
    fi
    ## check whether installed or not
    local basedir=''
    #for dir in `echo $VERSIONSWITCH_PATH | sed 's/:/ /g'`; do
    for dir in `echo $VERSIONSWITCH_PATH | awk -F: '{for(i=1;i<=NF;i++){print $i}}'`; do
        if [ -n "$dir" -a -d "$dir/$lang" ]; then
            basedir="$dir/$lang"
            break
        fi
    done
    if [ -z "$basedir" ]; then
        echo "versionswitch: $lang is not installed."
        return 1
    fi
    ## list available versions if version is not specified
    local dir
    local ver
    if [ -z "$version" ]; then
        echo "## basedir: $basedir"
        echo "## versions:"
        for dir in `echo "$basedir/*/bin"`; do
            dir=`dirname $dir`
            ver=`basename $dir`
            [ "$ver" != '*' ] && echo $ver
        done
        return 0
    fi
    ## find 'bin' directory
    local bindir
    if [ "$version" = "-" ]; then
        bindir=""
    elif [ "$version" = "latest" ]; then
        #bindir=`/bin/ls -d $basedir/*/bin 2>/dev/null | /usr/bin/tail -1`
        bindir=`echo $basedir/*/bin | awk '{print $NF}'`
        [ "$bindir" = "$basedir/*/bin" ] && bindir=""
    else
        bindir="$basedir/$version/bin"
        #[ -d "$bindir" ] || bindir=`/bin/ls -d $basedir/$version*/bin | /usr/bin/tail -1`
        if ! [ -d "$bindir" ]; then
            bindir=`echo $basedir/$version*/bin | awk '{print $NF}'`
            [ "$bindir" = "$basedir/$version*/bin" ] && bindir=""
        fi
    fi
    if [ -z "$bindir" -a "$version" != "-" ]; then
        echo "versionswitch: $lang version $version is not installed."
        return 1
    fi
    ## remove current bindir from $PATH
    #local path=`ruby -e "print ENV['PATH'].split(':').delete_if{|x|x=~%r'^$basedir/.*/bin'}.join(':')"`
    local newpath=`echo $PATH | awk -F: '{
        path = "";
        rexp = "^'$basedir'/";
        for (i = 1; i <= NF; i++) {
            if (! match($i, rexp)) {
                path = path ? path ":" $i : $i;
            }
        }
        print path;
    }'`
    ## set $PATH
    local prompt='$'  # or '[versionswitch]$'
    [ -n "$bindir" ] && newpath=$bindir:$newpath
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
