###
### $Release: 0.0.0 $
### $License: Public Domain $
###

###
### versionswitcher.sh -- switch version of language or application
###
### Setup example:
###   $ VS_HOME=$HOME/vs
###   $ . ~/.vs/scripts/versionswitcher.sh'
###   $ vs --help
###

__vs_version=`echo '$Release: 0.0.0 $' | awk '{print $2}'`


###
[ -z "$VS_HOME" -a -d $HOME/vs ] && VS_HOME=$HOME/vs


###
__vs_help_message() {
        cat <<END
versionswitcher - change version of language or application
Release: $release
Usage: vs [options] [lang] [version]
   -h                       : help
   -v                       : version
   -i [lang] [version]      : install
   -u                       : self upgrade
   -q                       : quiet
   -x lang version          : execute language command
   -X lang version command  : execute specific command

Examples:
   $ VS_HOME=\$HOME/lang
   $ vs -h               # show help
   $ vs                  # list language names installed
   $ vs python           # list python vesrions installed
   $ vs python 3.4.0     # use \$VS_HOME/python/3.4.0
   $ vs python 3         # use \$VS_HOME/python/3.x.x (ex. 3.4.5)
   $ vs python latest    # use latest version under \$VS_HOME/python
   $ vs python -         # use system-installed one (ex. /usr/bin/python)
   $ vs -i               # list language names installable
   $ vs -i python        # list python versions installable
   $ vs -i python 3.4.5  # install python 3.4.5 ('latest' is not available!)
   $ vs -x python 3.4.5       # execute \$VS_HOME/python/3.4.5/python
   $ vs -X python 3.4.5 2to3  # execute \$VS_HOME/python/3.4.5/2to3

Tips:
   * Short name 'vs' is an alias to 'versionswitcher'.
   * \$HOME/.vs/hooks/<language>.sh is imported if exists.
   * 'vs (py|rb|pl|gosh)' are available instead of
     'vs (python|ruby|perl|gauche)'.
     For example:
        $ vs py latest   # same as vs python latest
END
#    * It is allowed to set VS_HOME=path1:path2:path3:...
}


###
versionswitcher() {
    local lang
    local command
    local version
    local release=`echo '$Release: 0.0.0 $' | awk '{print $2}'`
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
    -u|--upgrade)
        __vs_upgrade
        ;;
    -x|--execute)
        shift                 # ignore option
        __vs_execute -x "$@"
        ;;
    -X|--execute-command)
        shift                 # ignore option
        __vs_execute -X "$@"
        ;;
    -*)
        echo "versionswitcher: $1: unknown option." 1>&2
        ;;
    *)
        lang="$1"
        version="$2"
        lang=`__vs_lang_name "$lang"`
        __vs_switch "$lang" "$version"
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
        [ "$filenames" = "$pattern" ] || echo $filenames
    fi
}


###
__vs_echo() {
    if [ -z "$__vs_option_quiet" ]; then
        echo "$1"
    fi
}


###
__vs_lang_name() {             # you can override this in your .bashrc
    __vs_lang_name__ "$1"
}
__vs_lang_name__() {
    case "$1" in
    py)      echo 'python'   ;;
    rb)      echo 'ruby'     ;;
    rbx)     echo 'rubinius' ;;
    pl)      echo 'perl'     ;;
    gosh)    echo 'gauche'   ;;
    *)       echo "$lang"    ;;
    esac
}


###
__vs_command_name() {          # you can override this in your .bashrc
    __vs_command_name__ "$1"
}
__vs_command_name__() {
    case "$1" in
    rubinius)  echo 'rbx'    ;;
    gauche)    echo 'gosh'   ;;
    pypy3)     echo 'pypy'   ;;
    rust)      echo 'rustc'  ;;
    *)         echo "$lang"  ;;
    esac
}


###
__vs_downloader() {
    local curlopt=$1
    local wgetopt=$2
    local curl=`which curl`
    local wget=`which wget`
    local down
    if   [ -n "$curl" ]; then
        echo "curl $curlopt"
    elif [ -n "$wget" ]; then
        echo "wget $wgetopt"
    else
        echo "$prompt ERROR: 'wget' or 'curl' required." 1>&2
        return 1
    fi
}


###
__vs_versions() {
    local basedir=$1
    local version=$2
    local len
    __vs_glob "$basedir/$version*/bin" | awk '{
      for (i=1; i<=NF; i++) {
        binpath = $i;
        len = split(binpath, arr, "/");
        version = arr[len-1];
        len = split(version, nums, /[^0-9]+/);
        key = "";
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
    echo "versionswitcher: $msg" 1>&2
    return 1
}


###
__vs_switch() {
    local lang=$1
    local version=$2
    ## exit if $VS_HOME is not set
    [ -n "$VS_HOME" ] || __vs_error '$VS_HOME is not set.' || return 1
    ## show all language names if lang is not specified
    local dir
    local basedir
    local list
    if [ -z "$lang" ]; then
        #echo "## language          # basedir"
        __vs_echo "## installed"
        for dir in `echo $VS_HOME | tr ':' ' '`; do
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
    for dir in `echo $VS_HOME | tr ':' ' '`; do
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
    ## import hook script if exists
    local script="$HOME/.vs/hooks/$lang.sh"
    [ -f "$script" ] && . $script
}


###
__vs_download() {
    local filename=$1
    local url="http://versionswitcher.appspot.com/$filename"
    [ -n "$VS_DEBUG" ] && url="http://localhost:8080/$filename"
    [ -n "$VS_URL"   ] && url="$VS_URL/$filename"
    local vs_home="$HOME/.vs"
    local dir=`dirname $filename`
    [ "$dir" = "." ] && dir=""
    if [ -n "$dir" -a ! -d "$vs_home/$dir" ]; then
        mkdir -p $vs_home/$dir || __vs_error "Failed: mkdir -p $vs_home/$dir" || return 1
    fi
    local down
    down=`__vs_downloader '-sORL' '-qN'`     || return 1
    (cd $vs_home/$dir; eval $down $url) || __vs_error "Failed: $down $url" || return 1
    echo $vs_home/$filename
}


##
__vs_installable_langs() {
    local filepath="$HOME/.vs/data/INDEX.txt"
    [ -f "$filepath" ] || __vs_error "$filepath: not found." || return 1
    __vs_echo "## try 'vs -i LANG' where LANG is one of:"
    cat $filepath
}


##
__vs_installable_versions() {
    local lang=$1
    local printmsg=$2   # 'y' or 'n'
    local condense=$3   # 'y' or 'n'
    local url=''
    local url2=''
    local rexp=''
    local sep='.'
    local none='';
    #
    local fname="$HOME/.vs/data/$lang.txt"
    [ -f $fname ] || __vs_error "$lang: not supported ($fname not found)." || return 1
    . $fname
    #
    if [ "$printmsg" = 'y' ]; then
        [ -n "$url" ]  && echo "## checking $url"
        [ -n "$url2" ] && echo "## checking $url2"
        __vs_echo "## try 'vs -i $lang VERSION' where VERSION is one of:"
    fi
    #
    perl='perl';
    [ -f /usr/local/bin/perl ] && perl='/usr/local/bin/perl';
    [ -f /usr/bin/perl ]       && perl='/usr/bin/perl';
    #
    local down
    down=`__vs_downloader "-sL" "-q -O - --no-check-certificate"`          || return 1
    if [ "$condense" = 'y' ]; then
        eval $down $url $url2 | $perl -pe 's!</Key>!</Key>\n!g' | $perl -e '
            $sep  = "'$sep'";
            $rexp = q`'$rexp'`;
            $none = "'$none'";
            $lang = "'$lang'";
            my %verdict;
            for my $dir (split(/:/, $ENV{"VS_HOME"})) {
                $verdict{(split /[;\/]/, $_)[-2]} = 1 for (glob("$dir/$lang/*/bin"));
                #for my $path (glob("$dir/$lang/*/bin")) {
                #    my $version = (split(/[;\/]/, $path))[-2];
                #    $verdict{$version} = 1;
                #}
            }
            while (<>) {
                #push @{$d{$1}}, length($2) ? $2 : $none  if /$rexp/;
                if (/$rexp/) {
                    my $ver = $1;
                    my $none_ = $ver =~ m/(rc|beta)\d$/ ? "" : $none;  # for Go
                    my $patch = length($2) ? $2 : $none_;
                    my $v = length($patch) ? "$ver$sep$patch" : $ver;
                    push @{$d{$ver}}, (exists($verdict{$v}) ? "$patch*" : $patch);
                }
            }
            #sub norm { join ".", map { sprintf("%03d", $_) } split(/\./, $_[0]) }
            for (sort keys %d) {
                @arr = sort {$a<=>$b} @{$d{$_}};
                if    ($#arr)           { print $_, $sep, "{", join(",", @arr), "}\n"; }
                elsif ($arr[0] eq "*")  { print $_, "*\n"; }
                elsif (length($arr[0])) { print $_, $sep, $arr[0], "\n"; }
                else                    { print $_, "\n"; }
            }
        '
    else
        eval $down $url $url2 | $perl -e '
            $sep  = "'$sep'";
            $rexp = q`'$rexp'`;
            $none = "'$none'";
            while (<>) {
                #push @arr, (($v = $2 ne "" ? $2 : $none) ne "" ? "$1$sep$v" : $1) if /$rexp/;
                if (/$rexp/) {
                    my $ver   = $1;
                    my $patch = $2 ne "" ? $2 : $none;
                    push @arr, ($patch ne "" ? "$ver$sep$patch" : $ver);
                }
            }
            print $_, "\n" for sort @arr;
        '
    fi
    return 0
}


###
__vs_install() {
    local lang=$1
    local version=$2
    local filepath
    local prompt='**'
    local ret
    ## list all languages when lang is not specified
    if [ -z "$lang" ]; then
        __vs_installable_langs
        return 0
    fi
    ## expand shorter name
    lang=`__vs_lang_name "$lang"`
    ## show installable versions when version is not specified
    if [ -z "$version" ]; then
        __vs_installable_versions "$lang" y y
        return 0
    fi
    ## verify version
    local input
    local found=""
    local ver
    for ver in `__vs_installable_versions $lang n n`; do
        [ "$ver" = "$version" ] && found=true
    done
    if [ -z "$found" ]; then
        echo -n "$prompt Are you really to install $lang $version? [y/N]: "
        read input
        [ -z "$input" ] && input="n"
        case "$input" in
        y*|Y*)  ;;
        *)      return 1;;
        esac
    fi
    ## download installer script (if $VS_DOWNLOAD_INSTALLER is set)
    local script_file
    if [ -n "$VS_DOWNLOAD_INSTALLER" ]; then
        script_file=`__vs_download installers/vs_install_$lang.sh`
    else
        script_file="$HOME/.vs/installers/vs_install_$lang.sh"
    fi
    [ -f "$script_file" ] || __vs_error "$lang is not supported to install." || return 1
    ## confirm PREFIX directory
    [ -n "$VS_HOME" ] || __vs_error "Set \$VS_HOME before installation." || return 1
    local inst_dir=`echo $VS_HOME | awk -F: '{print $1}'`
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
    echo "$prompt vs $lang $version"  ; versionswitcher "$lang" "$version"
}


###
__vs_upgrade() {
    local site="http://versionswitcher.appspot.com"
    [ -n "$VS_DEBUG" ] && site="http://localhost:8080"
    [ -n "$VS_URL"   ] && site="$VS_URL"
    local down
    down=`__vs_downloader '-sL' '-q -O -'`         || return 1
    local ver=`eval $down $site/version`
    if [ "$ver" = "$__vs_version" -a -z "$VS_DEBUG" ]; then
        __vs_echo "current version is newest. exist."
    else
        __vs_echo "upgrade to $ver (current: $__vs_version)"
        local dir=$HOME/.vs/scripts
        mkdir -p $dir
        down=`__vs_downloader "-ORL" ""`           || return 1
        (cd $dir; rm -f install.sh; eval $down $site/install.sh)
        if [ -n "$BASH_VERSION" ]; then            # for bash
            bash $dir/install.sh
        elif [ -n "$ZSH_VERSION" ]; then           # for zsh
            zsh $dir/install.sh
        fi
        __vs_echo ". $dir/versionswitcher.sh"
        . $dir/versionswitcher.sh
    fi
}


###
__vs_execute() {
    local opt="$1"
    local lang="$2"
    local version="$3"
    local command=''
    if [ $opt = '-X' ]; then
        command="$4"
        shift
    fi
    shift
    shift
    shift
    ## exit if $VS_HOME is not set
    [ -n "$VS_HOME" ] || __vs_error '$VS_HOME is not set.' || return 1
    ## list all languages when lang is not specified
    if [ "$opt" = '-x' ]; then
        if [ -z "$lang" -o -z "$version" ]; then
            echo "Usage: vs -x lang version [arg1 arg2 ...]"
            echo "Example:"
            echo "   $ vs -x python 3.4.0"
            echo "         # execute \$VS_HOME/python/3.4.0/bin/python"
            echo "   $ vs -x python 3.4.0 file.py arg1 arg2"
            echo "         # execute \$VS_HOME/python/3.4.0/bin/python file.py arg1 arg2"
            return 0
        fi
    fi
    if [ "$opt" = '-X' ]; then
        if [ -z "$lang" -o -z "$version" -z "$command" ]; then
            echo "Usage: vs -X lang version command [arg1 arg2 ...]"
            echo "Example:"
            echo "   $ vs -x ruby 2.1.0 irb"
            echo "         # execute \$VS_HOME/ruby/2.1.2/bin/irb"
            echo "   $ vs -x ruby 2.1.0 gem install foobar"
            echo "         # execute \$VS_HOME/ruby/2.1.0/bin/gem install foobar"
            return 0
        fi
    fi
    ## normalized language name
    lang=`__vs_lang_name $lang`
    ## command name
    if [ "$opt" = '-x' ]; then
        command=`__vs_command_name $lang`
    fi
    ## check whether installed or not
    local basedir=''
    for dir in `echo $VS_HOME | tr ':' ' '`; do
        if [ -n "$dir" -a -d "$dir/$lang" ]; then
            basedir="$dir/$lang"
            break
        fi
    done
    [ -n "$basedir" ] || __vs_error "$lang is not installed." || return 1
    ## find 'bin' directory
    local bindir
    local ver
    if [ "$version" = "-" ]; then
        __vs_error "version should not be '-'\n"
        return 1
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
    [ -n "$bindir" ] || __vs_error "$lang version $version is not installed." || return 1
    ## execute command
    $bindir/$command "$@"
}


###
#alias vs=versionswitcher
vs() {
    versionswitcher "$@"
}
