vs() {
    if [ -f "$HOME/.vs/scripts/versionswitcher.sh" ]; then
        . $HOME/.vs/scripts/versionswitcher.sh
        versionswitcher $@
    else
        echo "*** ERROR: versionswitcher.sh not found." 2>&1
        return 1
    fi
}
