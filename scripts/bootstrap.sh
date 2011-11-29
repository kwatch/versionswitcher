vs() {
    if [ -f "$HOME/.vs/scripts/versionswitcher.sh" ]; then
        . $HOME/.vs/scripts/versionswitcher.sh
        versionswitcher $@
    else
        echo "*** ERROR: versionswitcher.sh not found." 1>&2
        return 1
    fi
}
