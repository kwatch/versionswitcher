###
### $Release: 0.0.0 $
### $Copyright: copyright(c) 2011 kuwata-lab.com all rights reserved $
### $License: Public Domain $
###

###
### install.sh - install or upgrade VersionSwitcher
###
### usage:
###    $ wget http://versionswitcher.appspot.com/install.sh
###    $ #curl -O http://versionswitcher.appspot.com/install.sh
###    $ bash install.sh    # when you are bash user
###    $ #zsh install.sh    # when you are zsh user
###

_cmd() {
    echo '$' $1
    if eval $1; then
        return 0
    else
        echo "** FAILED: $1" 2>&1
        return 1
    fi
}


vs_install() {
    local install_sh=$1
    ## settings
    local vs_home="$HOME/.vs"
    local vs_url="http://versionswitcher.appspot.com"
    [ -n "$VS_DEBUG" ] && vs_url="http://localhost:8080"
    local prompt="***"
    ## detect 'wget' or 'curl' command
    local curl=`which curl`
    local wget=`which wget`
    local down
    if   [ -n "$curl" ]; then  down="curl -sORL"
    elif [ -n "$wget" ]; then  down="wget -q"
    else
        echo "$prompt ERROR: 'wget' or 'curl' required." 2>&1
        return 1
    fi
    ## create versionswitcher directory
    [ ! -d $vs_home            ] && _cmd "mkdir $vs_home"
    [ ! -d $vs_home/scripts    ] && _cmd "mkdir $vs_home/scripts"
    [ ! -d $vs_home/hooks      ] && _cmd "mkdir $vs_home/hooks"
    [ ! -d $vs_home/data       ] && _cmd "mkdir $vs_home/data"
    [ ! -d $vs_home/installers ] && _cmd "mkdir $vs_home/installers"
    ## copy install.sh into ~/.vs/scripts/
    if [ "$install_sh" != "$HOME/.vs/scripts/install.sh" ]; then
        _cmd "cp -p $install_sh $vs_home/scripts/"          || return 1
    fi
    ## download scripts
    _cmd "cd $vs_home/scripts"                              || return 1
    _cmd "$down $vs_url/scripts/versionswitcher.sh"         || return 1
    _cmd "$down $vs_url/scripts/bootstrap.sh"               || return 1
    ## download data files
    _cmd "cd $vs_home/data"                                 || return 1
    _cmd "$down $vs_url/data/INDEX.txt"                     || return 1
    langs=`cat INDEX.txt | awk '{print $1}'`
    for lang in `echo $langs`; do
        _cmd "$down $vs_url/data/$lang.txt"                 || return 1
    done
    ## download language installers
    _cmd "cd $vs_home/installers"                           || return 1
    _cmd "$down $vs_url/installers/vs_install.sh"           || return 1
    for lang in `echo $langs`; do
        _cmd "$down $vs_url/installers/vs_install_$lang.sh" || return 1
    done
    ## download hook script examples
    _cmd "cd $vs_home/hooks"                                || return 1
    for lang in "python" "ruby"; do
        if [ ! -f "$lang.sh" ]; then
            _cmd "$down $vs_url/hooks/$lang.sh"             || return 1
        fi
    done
    ## detect bash or zsh
    if   [ -n "$BASH_VERSION" ]; then  shell="bash"
    elif [ -n "$ZSH_VERSION"  ]; then  shell="zsh"
    elif [ -f "$HOME/.zshrc"  ]; then  shell="zsh"
    elif [ -f "$HOME/.bashrc" ]; then  shell="bash"
    else                               shell="bash"
    fi
    local rcfile=".${shell}rc"
    ## add settings into .bashrc or .zshrc
    if [ -z "$VS_PATH" ]; then
        echo "$prompt"
        echo "$prompt You have to write following lines into your ~/$rcfile:"
        echo "$prompt"
        echo "$prompt     export VS_PATH=\$HOME/langs     # or other directories"
        echo "$prompt     . \$HOME/.vs/scripts/bootstrap.sh"
        echo "$prompt"
        echo -n "$prompt Do you want to add above lines into your ~/$rcfile? [Y/n]: "
        local input=""
        read input; [ -z "$input" ] && input="y"
        case "$input" in
        y*|Y*)
            echo "export VS_PATH=\$HOME/langs   # or other directories" >> $HOME/$rcfile
            echo ". \$HOME/.vs/scripts/bootstrap.sh" >> $HOME/$rcfile
            echo "$prompt"
            echo "$prompt You should log out or restart $shell to enable settings."
            ;;
        *)
            echo "$prompt"
            echo "$prompt After adding the above lines into your ~/$rcfile,"
            echo "$prompt you should log out or restart $shell to enable settings."
            ;;
        esac
    fi
    ## finish
    echo "$prompt"
    echo "$prompt Installation is finished successfully."
    echo "$prompt See $vs_url/ for details."
    echo "$prompt Thank you."
}


if [ "root" = `whoami` ]; then
    echo "*** not allowed to execute by root user!" 2>&1
    echo "*** exit 1" 2>&1
    exit 1
fi
vs_install "$0"
