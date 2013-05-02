local P_USER_AT="%B(%b%(!.%F{red}%U.%F{blue})%n%(!.%u.)%f%B@%b%F{yellow}%m%f%B)%b"
local P_CURDIR="%B(%b%F{green}%~%f%B)%b"
local P_TIME="%B(%b%F{magenta}%D{%a %Y-%m-%d}%f %F{cyan}%D{%r}%f%B)%b"

function prompt_aws_context() {
    if [[ -n ${AWS_DEFAULT_REGION} ]] && [[ -e ${AWS_CONFIG_FILE} ]]
    then
        local aws_promptstring
        aws_promptstring='%B%F{green}aws(%f%b'
        aws_promptstring="${aws_promptstring}%F{red}\${AWS_CONFIG_FILE:t}%f"
        aws_promptstring="${aws_promptstring}%B@%b"
        aws_promptstring="${aws_promptstring}%F{yellow}\${AWS_DEFAULT_REGION}%f"
        aws_promptstring="${aws_promptstring}%B%F{green})%f%b"
        export P_AWS_CONTEXT=${aws_promptstring}
        unset aws_promptstring
    else
        unset P_AWS_CONTEXT
        unset aws_promptstring
    fi
}
add-zsh-hook precmd prompt_aws_context

autoload -Uz vcs_info
zstyle ':vcs_info:*' enable git
zstyle ':vcs_info:git*' check-for-changes true
zstyle ':vcs_info:git*' unstagedstr '%B%F{yellow}☻%f%b '
zstyle ':vcs_info:git*' stagedstr '%B%F{green}☻%f%b '
function +vi-git-st() {
    local ahead behind
    local -a gitstatus

    # for git prior to 1.7
    # ahead=$(git rev-list origin/${hook_com[branch]}..HEAD | wc -l)
    ahead=$(git rev-list ${hook_com[branch]}@{upstream}..HEAD 2>/dev/null | wc -l)
    (( $ahead )) && gitstatus+=( "%F{magenta}↑${ahead//[[:space:]]/}%f" )

    # for git prior to 1.7
    # behind=$(git rev-list HEAD..origin/${hook_com[branch]} | wc -l)
    behind=$(git rev-list HEAD..${hook_com[branch]}@{upstream} 2>/dev/null | wc -l)
    (( $behind )) && gitstatus+=( "%F{magenta}↓${behind//[[:space:]]/}%f" )

    hook_com[misc]+=${(j:/:)gitstatus}
}
function +vi-git-remotebranch() {
    local remote

    # Are we on a remote-tracking branch?
    remote=${$(git rev-parse --verify ${hook_com[branch]}@{upstream} \
        --symbolic-full-name 2>/dev/null)/refs\/remotes\/}

    if [[ -n ${remote} ]] ; then
        hook_com[branch]="${hook_com[branch]}<${remote}>"
    fi
}
zstyle ':vcs_info:git*+set-message:*' hooks git-st git-remotebranch

zstyle ':vcs_info:git*' formats \
    " %B%F{blue}%s(%f%F{green}%r[%f%F{red}%b:%m %u%c%f%F{green}]%f%F{blue})%f%%b"
zstyle ':vcs_info:git*' actionformats \
    " %B%F{blue}%s(%f%F{green}%r[%f%F{red}%b|%a:%m %u%c%f%F{green}]%f%F{blue})%f%%b"
add-zsh-hook precmd vcs_info

PROMPT="
${P_TIME}${P_AWS_CONTEXT}
${P_CURDIR}\${vcs_info_msg_0_}
%# "
RPROMPT="${P_USER_AT}"

# vim: ft=zsh sw=4 sts=4 ts=4 expandtab
