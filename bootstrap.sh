vs() {
    if [ -f "$HOME/.versionswitcher/versionswitcher.sh" ]; then
        . $HOME/.versionswitcher/versionswitcher.sh
        versionswitcher $@
    else
        echo "*** ERROR: versionswitcher.sh not found." 2>&1
        return 1
    fi
}
