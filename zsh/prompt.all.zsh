P_USER_AT="%B(%b%(!.%F{red}%U.%F{blue})%n%(!.%u.)%f%B@%b%F{yellow}%m%f%B)%b"
P_CURDIR="%B(%b%F{green}%~%f%B)%b"
P_TIME="%B(%b%F{magenta}%D{%a %Y-%m-%d}%f %F{cyan}%D{%r}%f%B)%b"

autoload -Uz vcs_info
zstyle ':vcs_info:*' enable git
zstyle ':vcs_info:git*' check-for-changes true
zstyle ':vcs_info:git*' unstagedstr '%B%F{yellow}☻%f%b '
zstyle ':vcs_info:git*' stagedstr '%B%F{green}☻%f%b '
zstyle ':vcs_info:git*+set-message:*' hooks git-st
function +vi-git-st() {
    local ahead behind
    local -a gitstatus

    # for git prior to 1.7
    # ahead=$(git rev-list origin/${hook_com[branch]}..HEAD | wc -l)
    ahead=$(git rev-list ${hook_com[branch]}@{upstream}..HEAD 2>/dev/null | wc -l)
    (( $ahead )) && gitstatus+=( "↑${ahead}" )

    # for git prior to 1.7
    # behind=$(git rev-list HEAD..origin/${hook_com[branch]} | wc -l)
    behind=$(git rev-list HEAD..${hook_com[branch]}@{upstream} 2>/dev/null | wc -l)
    (( $behind )) && gitstatus+=( "↓${behind}" )

    hook_com[misc]+=${(j:/:)gitstatus}
}
zstyle ':vcs_info:git*+set-message:*' hooks git-remotebranch
function +vi-git-remotebranch() {
    local remote

    # Are we on a remote-tracking branch?
    remote=${$(git rev-parse --verify ${hook_com[branch]}@{upstream} \
        --symbolic-full-name 2>/dev/null)/refs\/remotes\/}

    if [[ -n ${remote} ]] ; then
        hook_com[branch]="${hook_com[branch]}<${remote}>"
    fi
}

zstyle ':vcs_info:git*' formats \
    " %B%F{blue}%s(%f%F{green}%r[%f%F{red}%b:%m %u%c%f%F{green}]%f%F{blue})%f%%b"
zstyle ':vcs_info:git*' actionformats \
    " %B%F{blue}%s(%f%F{green}%r[%f%F{red}%b|%a:%m %u%c%f%F{green}]%f%F{blue})%f%%b"
add-zsh-hook precmd vcs_info

PROMPT="
${P_TIME}
${P_CURDIR}\${vcs_info_msg_0_}
%# "
RPROMPT="${P_USER_AT}"

# vim: ft=zsh sw=4 sts=4 ts=4 expandtab
