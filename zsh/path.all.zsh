typeset -U path
typeset -U manpath

path=( /usr/local/bin /usr/bin /bin /usr/local/sbin /usr/sbin /sbin )

manpath=( /usr/local/share/man /usr/share/man )

if [[ -n ${JAVA_HOME} ]]
then
    path=( ${JAVA_HOME}/bin(N/) ${path} )
fi

path=( ${DOTFILES}/bin(N/) ${path} )

# vim: filetype=zsh:ts=4:sw=4:expandtab
