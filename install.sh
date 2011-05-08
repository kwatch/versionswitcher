###
### $Date: $
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
    ## settings
    vs_home="$HOME/.versionswitcher"
    vs_url="http://versionswitcher.appspot.com"
    [ -n "$VS_DEBUG" ] && vs_url="http://localhost:8080"
    prompt="***"
    ## detect 'wget' or 'curl' command
    wget_path=`which wget`
    curl_path=`which curl`
    if   [ -n "$wget_path" ]; then  wget="wget -qN"
    elif [ -n "$curl_path" ]; then  wget="curl -OR"
    else
        echo "$prompt ERROR: 'wget' or 'curl' required." 2>&1
        return 1
    fi
    ## create versionswitcher directory
    [ ! -d $vs_home          ] && _cmd "mkdir $vs_home"
    [ ! -d $vs_home/versions ] && _cmd "mkdir $vs_home/versions"
    [ ! -d $vs_home/scripts  ] && _cmd "mkdir $vs_home/scripts"
    [ ! -d $vs_home/hooks    ] && _cmd "mkdir $vs_home/hooks"
    ## download scripts
    _cmd "cd $vs_home"                                      || return 1
    _cmd "$wget $vs_url/versionswitcher.sh"                 || return 1
    _cmd "$wget $vs_url/bootstrap.sh"                       || return 1
    ## download version files
    _cmd "cd $vs_home/versions"                             || return 1
    _cmd "$wget $vs_url/versions/INDEX.txt"                 || return 1
    langs=`cat INDEX.txt | awk '{print $1}'`
    for lang in `echo $langs`; do
        _cmd "$wget $vs_url/versions/$lang.txt"             || return 1
    done
    ## download installer scripts
    _cmd "cd $vs_home/scripts"                              || return 1
    for lang in `echo $langs`; do
        _cmd "$wget $vs_url/scripts/vs_install_$lang.sh"    || return 1
    done
    ## detect bash or zsh
    if   [ -n "$BASH_VERSION" ]; then  shell="bash"
    elif [ -n "$ZSH_VERSION"  ]; then  shell="zsh"
    elif [ -f "$HOME/.zshrc"  ]; then  shell="zsh"
    elif [ -f "$HOME/.bashrc" ]; then  shell="bash"
    else                               shell="bash"
    fi
    rcfile=".${shell}rc"
    ## add settings into .bashrc or .zshrc
    echo "$prompt"
    echo "$prompt You have to write the following lines into your ~/$rcfile:"
    echo "$prompt"
    echo "$prompt     VERSIONSWITCHER_PATH=\$HOME/langs     # or other directories"
    echo "$prompt     . \$HOME/.versionswitcher/bootstrap.sh"
    echo "$prompt"
    echo -n "$prompt Do you want to add above lines into your ~/$rcfile? [Y/n]: "
    input=""
    read input; [ -z "$input" ] && input="y"
    case "$input" in
    y*|Y*)
        echo "VERSIONSWITCHER_PATH=\$HOME/langs   # or other directories" >> $HOME/$rcfile
        echo ". \$HOME/.versionswitcher/bootstrap.sh" >> $HOME/$rcfile
        echo "$prompt"
        echo "$prompt You should log out or restart $shell to enable settings."
        ;;
    *)
        echo "$prompt"
        echo "$prompt After adding the above lines into your ~/$rcfile,"
        echo "$prompt you should log out or restart $shell to enable settings."
        ;;
    esac
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
vs_install