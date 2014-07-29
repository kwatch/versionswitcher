###
### This file will be imported by vs command after switching Go version.
###
#if [ -n "$goversion" ]; then
#    PS1="Go-$goversion> "
#else
#    PS1="> "
#fi

echo "\$ export GOROOT=$goroot"
export GOROOT="$goroot"

