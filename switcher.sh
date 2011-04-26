##
## switcher.sh -- switch version of language or application
##
## installation:
##   $ echo '. /usr/local/bin/switcher.sh'
##   $ sw --help
##


##
#[ -z "$SWITCHER_PATH" ] && SWITCHER_PATH=$HOME/local/lang


##
switcher () {
    local lang=$1
    local version=$2
    local release=`echo '$Release: 0.1.0 $' | awk '{print $2}'`
    case $lang in
        -h|--help)
            cat <<END
switcher - change version of language or application
release: $release
examples:
    $ SWITCHER_PATH=\$HOME/local/lang
    $ sw foobar 1.2.3   # use \$HOME/local/lang/foobar/1.2.3
    $ sw foobar 1.2     # use \$HOME/local/lang/foobar/1.2.x (ex. 1.2.8)
    $ sw foobar latest  # use latest version under \$HOME/local/lang/foobar
    $ sw foobar -       # use system-installed (ex. /usr/bin/foobar)
    $ sw foobar         # show installed versions of foobar
    $ sw                # show installed languages

tips:
    * Short name 'sw' is an alias to 'switcher'.
    * It is allowed to set SWITCHER_PATH=path1:path2:path3:...
    * \$HOME/.switcher/hooks/<language>.sh is imported if exists.
END
            ;;
        -v|--version)
             echo $release
             ;;
        ruby|rb)       _switcher ruby      ruby     "$version";;
        python|py)     _switcher python    python   "$version";;
        perl)          _switcher perl      perl     "$version";;
        rubinius|rbx)  _switcher rubinius  rbx      "$version";;
        gauche|gosh)   _switcher gauche    gosh     "$version";;
        *)             _switcher $lang     $lang    "$version";;
    esac
}


##
_switcher () {
    local lang=$1
    local command=$2
    local version=$3
    ## show all language names if lang is not specified
    local dir
    local basedir
    local list
    if [ -z "$lang" ]; then
        #echo "## language          # basedir"
        echo "## installed"
        for dir in `echo $SWITCHER_PATH | awk -F: '{for(i=1;i<=NF;i++){print $i}}'`; do
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
    #for dir in `echo $SWITCHER_PATH | sed 's/:/ /g'`; do
    for dir in `echo $SWITCHER_PATH | awk -F: '{for(i=1;i<=NF;i++){print $i}}'`; do
        if [ -n "$dir" -a -d "$dir/$lang" ]; then
            basedir="$dir/$lang"
            break
        fi
    done
    if [ -z "$basedir" ]; then
        echo "switcher: $lang is not installed."
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
        echo "switcher: $lang version $version is not installed."
        return 1
    fi
    ## remove current bindir from $PATH
    #local path=`ruby -e "print ENV['PATH'].split(':').delete_if{|x|x=~%r'^$basedir/.*/bin'}.join(':')"`
    local path=`echo $PATH | awk -F: '{
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
    local prompt='$'  # or '[switcher]$'
    [ -n "$bindir" ] && path=$bindir:$path
    echo "$prompt export PATH=$path"     ; export PATH=$path
    hash -r
    ## set or clear ${lang}root
    local rootvar="${lang}root"
    #local vervar=`awk 'BEGIN{print toupper("SWITCHER_'$lang'_VERSION")}'`
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
    local script="$HOME/.switcher/hooks/$lang.sh"
    [ -f "$script" ] && . $script
}


##
alias sw=switcher
